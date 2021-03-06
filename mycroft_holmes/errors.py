"""
Exceptions thrown by mycroft_holmes
"""


class MycroftHolmesError(Exception):
    """
    A generic exception
    """


class MycroftSourceError(MycroftHolmesError):
    """
    Thrown when we fail to get a value from a source
    """


class MycroftMetricError(MycroftHolmesError):
    """
    Thrown when we fail to get a value for a metric
    """


class MycroftMetricsStorageError(MycroftHolmesError):
    """
    Thrown by MetricsStorage classes
    """
