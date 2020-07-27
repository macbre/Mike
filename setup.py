from setuptools import setup, find_packages

from mycroft_holmes import VERSION

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='mycroft_holmes',
    version=VERSION,
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    license='MIT',
    description='Mycroft Holmes (High-Optional, Logical, Multi-Evaluating Supervisor) aka Mike',
    keywords='',
    url='https://github.com/Wikia/Mike',
    packages=find_packages(),
    extras_require={
        'dev': [
            'coverage==5.2.1',
            'pylint>=2.4.2',
            'pytest==5.4.3',
        ]
    },
    install_requires=[
        'elasticsearch-query==2.4.0',
        'google-api-python-client==1.10.0',
        'mysql-connector-python==8.0.21',
        'oauthlib[signedtoken]>=2.1.0, <4.0.0',
        'requests-oauthlib==1.1.0',
        'jira==2.0.0',
        'PyAthena==1.11.0',
        'pyyaml>=4.2b1',
        'python-dotenv==0.14.0',
        'pyjq==2.4.0',
        'lxml>=4.2.0',
        # UI
        'flask==1.1.2',
        'gunicorn==20.0.4',
    ],
    entry_points={
        'console_scripts': [
            'collect_metrics=mycroft_holmes.bin.collect_metrics:main',
            'generate_source_docs=mycroft_holmes.bin.generate_source_docs:main',
        ],
    }
)
