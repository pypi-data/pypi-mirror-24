# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '2.0rc7'

long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()+ '\n'
)

setup(
    name='plone.app.mosaic',
    version=version,
    description='Plone Mosaic',
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='',
    author='',
    author_email='',
    url='https://github.com/plone/plone.app.mosaic',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.api',
        'plone.subrequest>=1.8',
        'plone.tiles>=1.8.3',
        'plone.app.blocks>=4.1.0',
        'plone.app.tiles>=3.0.3',
        'plone.app.drafts>=1.1.2',
        'plone.app.standardtiles>=2.2.0',
        'Products.CMFPlone>=5.0.4'
    ],
    extras_require={'test': [
        'plone.app.testing',
        'plone.app.contenttypes',
        'plone.app.widgets>=1.8.0.dev0',
        'plone.app.robotframework',
        'robotframework-selenium2library',
        'robotframework-selenium2screenshots'
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
