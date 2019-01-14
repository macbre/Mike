"""
Provides a blueprint that renders JSON with software version and environment details
"""
from flask import Blueprint, jsonify, render_template, url_for, abort

from mycroft_holmes.app.utils import get_config, get_feature_spec_by_id
from mycroft_holmes.storage import MetricsStorage

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/')
def index():
    """
    :rtype: flask.Response
    """
    config = get_config()
    storage = MetricsStorage(config=config)

    components = []

    for feature_name, feature_spec in config.get_features().items():
        feature_id = config.get_feature_id(feature_name)
        metrics = config.get_metrics_for_feature(feature_name)
        # print(feature_name, metrics)

        component = {
            'id': feature_id,

            # feature's metadata
            'name': feature_name,
            'docs': feature_spec.get('url'),
            'repo': feature_spec.get('repo'),

            # fetch metrics and calculated score
            'metrics': [
                metric.get_label_with_value() for metric in metrics if metric.value is not None
            ],
            'score': storage.get(feature_id, feature_metric='score'),

            # link to a feature's dashboard
            'url': url_for('dashboard.feature', feature_id=feature_id),
        }

        components.append(component)

    # sort components by score (descending)
    components = sorted(components, key=lambda item: item['score'], reverse=True)

    # print(components)

    return render_template(
        'index.html',
        components=components,
        _json=url_for('dashboard.index_json'),
    )


@dashboard.route('/index.json')
def index_json():
    """
    :rtype: flask.Response
    """
    config = get_config()
    storage = MetricsStorage(config=config)

    return jsonify({
        'dashboard_name': config.get_name(),
        'features': [
            {
                'name': feature_name,
                'url': feature_spec.get('url'),
                'repo': feature_spec.get('repo'),
                'metrics': [metric['name'] for metric in feature_spec['metrics']],
                'score': storage.get(
                    feature_id=config.get_feature_id(feature_name),
                    feature_metric='score'
                ),
                'links': {
                    'self': url_for('dashboard.index')
                }
            }
            for feature_name, feature_spec in config.get_features().items()
        ]
    })


@dashboard.route('/component/<string:feature_id>')
def feature(feature_id):
    """
    :type feature_id str
    :rtype: flask.Response
    """
    config = get_config()
    storage = MetricsStorage(config=config)

    # find a feature by ID
    feature_spec = get_feature_spec_by_id(config, feature_id)

    # not found? return 404
    if feature_spec is None:
        abort(404, 'Feature "%s" not found' % (feature_id,))

    metrics = [
        {
            'name': metric.get_name(),
            'source': metric.get_source_name(),
            'raw_value': metric.value,
            'value': metric.get_formatted_value(),
            'weight': metric.get_weight(),
            'label': metric.get_label(),
            'more_link': metric.get_more_link(),
        }
        for metric in config.get_metrics_for_feature(feature_spec['name'])
    ]

    return render_template(
        'feature.html',
        component=feature_spec,
        metrics=metrics,
        score=storage.get(feature_id, feature_metric='score'),
        _csv='#',
        _json='#',
    )
