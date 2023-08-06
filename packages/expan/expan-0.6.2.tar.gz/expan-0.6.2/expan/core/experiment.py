import logging
import re
import warnings

import numpy as np
import pandas as pd

import expan.core.binning as binmodule
import expan.core.early_stopping as es
import expan.core.statistics as statx

from expan.core.version import __version__

from expan.core.util import get_column_names_by_type
# from expan.core.experimentdata import ExperimentData
# from expan.core.results import Results, delta_to_dataframe_all_variants, feature_check_to_dataframe, \
#     early_stopping_to_dataframe

# from expan.core.jsonable import Jsonable

# raise the same warning multiple times
warnings.simplefilter('always', UserWarning)

logger = logging.getLogger(__name__)


# TODO: add filtering functionality: we should be able to operate on this
# class to exclude data points, and save all these operations in a log that then
# is preserved in all results.
class Experiment(object):
    """
    Class which adds the analysis functions to experimental data.
    """
    def __init__(self, control_variant_name, data, metadata, report_kpi_names=None, derived_kpis=None):
        report_kpi_names = report_kpi_names or []
        derived_kpis  = derived_kpis or []

        experiment_column_names = set(['entity', 'variant'])
        numerical_column_names  = set(get_column_names_by_type(data, np.number))

        if type(report_kpi_names) is str:
            report_kpi_names = [report_kpi_names]

        if type(report_kpi_names) is not list:
            raise TypeError('report_kpi_names should be a list of str')

        if report_kpi_names:
            report_kpi_names_needed = set(report_kpi_names)
        else:
            report_kpi_names_needed = numerical_column_names - experiment_column_names

        # check derived_kpis structure (should have keys namely 'name' and 'formula')
        for i in derived_kpis:
            if not isinstance(i, dict):
                raise TypeError('Derived kpis should be an array of dictionaries')
            if 'formula' not in i:
                raise KeyError('Dictionary should have key "formula"')
            if 'name' not in i:
                raise KeyError('Dictionary should have key "name"')

        derived_kpi_names    = [k['name']    for k in derived_kpis]
        derived_kpi_formulas = [k['formula'] for k in derived_kpis]

        # what columns do we expect to find in the data frame?
        required_column_names = (report_kpi_names_needed | experiment_column_names) - set(derived_kpi_names)
        kpi_name_pattern = '([a-zA-Z][0-9a-zA-Z_]*)'
        # add names from all formulas
        for formula in derived_kpi_formulas:
            names = re.findall(kpi_name_pattern, formula)
            required_column_names = required_column_names | set(names)

        for c in required_column_names:
            if c not in data:
                raise ValueError('No column %s provided'%c)

        self.data                 =     data.copy()
        self.metadata             = metadata.copy()
        self.report_kpi_names     = report_kpi_names_needed
        self.derived_kpis         = derived_kpis
        self.variant_names        = set(self.data.variant)
        self.control_variant_name = control_variant_name
        self.reference_kpis       = {}

        # add derived KPIs to the data frame
        for name, formula in zip(derived_kpi_names, derived_kpi_formulas):
            self.data.loc[:, name] = eval(re.sub(kpi_name_pattern, r'self.data.\1.astype(float)', formula))
            self.reference_kpis[name] = re.sub(kpi_name_pattern + '/', '', formula)

    def get_kpi_by_name_and_variant(self, name, variant):
        return self.data.reset_index().set_index('variant').loc[variant, name]

    def __str__(self):
        variants = self.variant_names

        return 'Experiment "{:s}" with {:d} derived kpis, {:d} report kpis, {:d} entities and {:d} variants: {}'.format(
            self.metadata['experiment'], len(self.derived_kpis), len(self.report_kpi_names), len(self.data),
            len(variants), ', '.join([('*' + k + '*') if (k == self.control_variant_name) else k for k in variants]))

    def _get_weights(self, kpi, variant):
        if kpi not in self.reference_kpis:
            return 1.0
        reference_kpi  = self.reference_kpis[kpi]
        x              = self.get_kpi_by_name_and_variant(reference_kpi, variant)
        zeros_and_nans = sum(x == 0) + np.isnan(x).sum()
        non_zeros      = len(x) - zeros_and_nans
        return non_zeros/np.nansum(x) * x

    def delta(self, method='fixed_horizon', **worker_args):
        worker_table = {
                'fixed_horizon'    : statx.make_delta,
                'group_sequential' : es.make_group_sequential,
                'bayes_factor'     : es.make_bayes_factor,
                'bayes_precision'  : es.make_bayes_precision,
                }

        if not method in worker_table:
            raise NotImplementedError

        worker = worker_table[method](**worker_args)

        result = {}
        result['warnings']        = []
        result['errors']          = []
        result['expan_version']   = __version__
        result['control_variant'] = self.control_variant_name
        kpis = []

        for kpi in self.report_kpi_names:
            res = {}
            res['name']     = kpi
            res['variants'] = []
            control       = self.get_kpi_by_name_and_variant(kpi, self.control_variant_name)
            controlWeight = self._get_weights(kpi, self.control_variant_name)
            for variant in self.variant_names:
                treatment       = self.get_kpi_by_name_and_variant(kpi, variant)
                treatmentWeight = self._get_weights(kpi, variant)
                with warnings.catch_warnings(record=True) as w:
                    ds = worker(x=treatment*treatmentWeight, y=control*controlWeight)
                if len(w):
                    result['warnings'].append('kpi: ' + kpi + ', variant: '+ variant + ': ' + str(w[-1].message))
                res['variants'].append({'name'             : variant,
                                        'delta_statistics' : ds})
            kpis.append(res)

        result['kpis'] = kpis
        return result

    def _quantile_filtering(self, kpis, percentile, threshold_type):
        method_table = {'upper': lambda x: x > threshold, 'lower': lambda x: x <= threshold}
        flags = pd.Series(data=[False]*len(self.data))
        for column in self.data[kpis].columns:
            threshold = np.percentile(self.data[column], percentile)
            flags = flags | self.data[column].apply(method_table[threshold_type])
        return flags

    def filter(self, kpis, percentile=99.0, threshold_type='upper'):
        """
        Method that filters out entities whose KPIs exceed the value at a given percentile.
        If any of the KPIs exceeds its threshold the entity is filtered out.

        Args:
            kpis (list): list of KPI names
            percentile (float): percentile considered as threshold
            threshold_type (string): type of threshold used ('lower' or 'upper')

        Returns:

        """

        # check if provided KPIs are present in the data
        for kpi in kpis:
            if kpi not in self.data.columns:
                raise KeyError(kpi + ' identifier not present in dataframe columns!')

        # check if provided percentile is valid
        if 0.0 < percentile <= 100.0 is False:
            raise ValueError("Percentile value needs to be between 0.0 and 100.0!")

        # check if provided filtering kind is valid
        if threshold_type not in ['upper', 'lower']:
            raise ValueError("Threshold type needs to be either 'upper' or 'lower'!")

        # run quantile filtering
        flags = self._quantile_filtering(kpis=kpis, percentile=percentile, threshold_type=threshold_type)

        # log which columns were filtered and how many entities were filtered out
        self.metadata['filtered_columns'] = kpis
        self.metadata['filtered_entities_number'] = len(flags[flags == True])
        self.metadata['filtered_threshold_kind'] = threshold_type

        # throw warning if too many entities have been filtered out
        if (len(flags[flags == True]) / float(len(self.data))) > 0.02:
            warnings.warn('More than 2% of entities have been filtered out, consider adjusting the percentile value.')

        self.data = self.data[flags == False]
