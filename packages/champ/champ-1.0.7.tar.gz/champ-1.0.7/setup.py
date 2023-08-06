from setuptools import setup

options=dict( name='champ',
    version='1.0.7',
    packages=['champ'],
    url='http://github.com/wweir827/champ',
    license='GPLv3+',
    author='William H. Weir',
    provides=['champ'],
    author_email='wweir@med.unc.edu',
    description='Modularity based networks partition selection tool',
    zip_safe=False,
    classifiers=["Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.3",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                 "Topic :: Scientific/Engineering :: Information Analysis",
                 ],
    install_requires=['ipython<5.9','pyhull','matplotlib','future','numpy>1.13','h5py',
                      'scipy','sklearn','louvain','python-igraph']
)
#    install_requires=['pyhull','igraph','louvain','matplotlib','numpy',]

setup(**options)
