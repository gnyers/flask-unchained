from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Flask Unchained',
    version='0.5.1',
    description='The better way to build large Flask applications',
    long_description=long_description,
    url='https://github.com/briancappello/flask-unchained',
    author='Brian Cappello',
    license='MIT',

    packages=find_packages(exclude=['docs', 'tests']),
    py_modules=['flask_mail'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'blinker>=1.4',
        'flask>=0.12.2',
        'flask_babelex>=0.9.3',
        'flask_wtf',
        'networkx>=2.1',
    ],
    extras_require={
        'admin': [
            'flask-admin',
        ],
        'api': [
            'apispec>=0.39.0',
            'flask-marshmallow>=0.8.0',
            'marshmallow>=2.13.6',
            'marshmallow-sqlalchemy>=0.13.1',
        ],
        'celery': [
            'celery',
            'dill',
            'redis',
        ],
        'dev': [
            'coverage',
            'factory_boy',
            'IPython',
            'm2r',
            'mock',
            'pytest',
            'pytest-flask',
            'tox',
        ],
        'docs': [
            'sphinx',
            'sphinx-autobuild',
            'sphinx-click',
            'sphinx-rtd-theme',
            'PyQt5',
            'qtconsole',
        ],
        'mail': [
            'beautifulsoup4>=4.6.0',
            'lxml>=4.2.1',
        ],
        'security': [
            'flask_security_bundle',
        ],
        'session': [
            'dill',
            'flask_session',
        ],
        'sqlalchemy': [
            'flask-migrate>=2.1.1',
            'flask-sqlalchemy>=2.3',
            'py-yaml-fixtures>=0.1.2',
        ],
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points='''
        [console_scripts]
        flask=flask_unchained.cli:main
        [pytest11]
        flask_unchained=flask_unchained.pytest
    ''',
)
