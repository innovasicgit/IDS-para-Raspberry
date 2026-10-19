from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


elimina = [
    'number__tcp_flags_cwr',
    'number__tcp_flags_ecn',
    'number__tcp_flags_urg',
    'number__tcp_flags_ack',
    'number__tcp_flags_push',
    'number__tcp_flags_reset',
    'number__tcp_flags_fin',
    'number__icmp_type',
    'number__ip_flags_rb',
    'number__tcp_flags_res',
]


class del_columns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        frame = pd.DataFrame(X, columns=self.columns)
        columns_to_drop = [column for column in elimina if column in frame.columns]
        return frame.drop(columns=columns_to_drop)

    def get_feature_names_out(self, input_features=None):
        features = self.columns if input_features is None else input_features
        return [feature for feature in features if feature not in elimina]
