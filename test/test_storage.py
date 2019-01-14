"""
Set of unit test for metrics storage
"""
from unittest import SkipTest

from os import environ

from mycroft_holmes.config import Config
from mycroft_holmes.metric import Metric
from mycroft_holmes.storage import MetricsStorage


class ConfigForMetricsStorage(Config):
    def __init__(self):
        self.data = {
            'storage': {
                'engine': 'mysql',
                'host': '127.0.0.1',
                'database': environ.get('TEST_DATABASE'),
                # TravisCI default values
                'user': environ.get('TEST_DATABASE_USER', 'root'),
                'password': environ.get('TEST_DATABASE_PASSWORD', ''),
            }
        }


def test_storage():
    if environ.get('TEST_DATABASE') is None:
        raise SkipTest('TEST_DATABASE env variable needs to be set to run this test.')

    storage = MetricsStorage(config=ConfigForMetricsStorage())

    # push some metrics and later on try to get them
    storage.push('foo', {'score': 123, 'bar/metric': 42.4})
    storage.push('bar', {'score': 1, 'bar/metric': -3})
    storage.commit()

    storage.push('bar', {'score': 5, 'bar/metric': -4})
    storage.commit()

    assert storage.get(feature_id='foo', feature_metric='score') == 123
    assert storage.get(feature_id='foo', feature_metric='bar/metric') == 42, 'Storage keeps integers'

    assert storage.get(feature_id='bar', feature_metric='score') == 5, 'The most recent value should be taken'
    assert storage.get(feature_id='bar', feature_metric='bar/metric') == -4, 'Negative values are accepted'

    assert storage.get(feature_id='not_existing', feature_metric='bar/metric') is None, 'Not existing metric'

    # now check if we can get the metric value
    metric = Metric(feature_name='Bar', config=ConfigForMetricsStorage(), spec={'name': 'bar/metric'})
    assert metric.value == -4, 'Get the most recent value from the storage'

    metric = Metric(feature_name='Foo', config=ConfigForMetricsStorage(), spec={'name': 'bar/metric'})
    assert metric.value == 42, 'Get the most recent value from the storage'