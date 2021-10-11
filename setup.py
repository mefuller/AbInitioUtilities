from setuptools import setup

setup(
    name='AbInitioUtilities',
    version='0.1.0',
    description='Helper programs/routines for ab initio calculations',
    url='https://github.com/mefuller/AbInitioUtilities',
    author='Mark E. Fuller',
    author_email='fuller@stossrohr.net',
    license='GPLv3+',
    packages=['AbInitioUtilities'],
    install_requires=['os',
                      'sys',
                      'numpy',
                      'collections',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
