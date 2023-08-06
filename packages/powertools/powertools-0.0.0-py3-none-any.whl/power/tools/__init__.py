#-- power.tools
"""--- Power.Tools
General-purpose Utility Library
"""

__setup__ = dict(
    name='powertools',
    packages=['power.tools',  'power.test'],
    version='0.0.0',
    description=__doc__,

    url='https://github.com/philipov/powertools',
    author='Philip Loguinov',
    author_email='philipov@gmail.com',


    requires=[
        'pytest',
        'colored_traceback',
        'colorama',
        'termcolor'
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Customer Service',

        'License :: Other/Proprietary License',

        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3.6'
    ]
)

__version__ = __setup__['version']

__test_setup__ = __setup__
