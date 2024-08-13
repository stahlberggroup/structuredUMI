#!/usr/bin/env python3
from setuptools import setup, find_packages

install_requires = ["numpy","matplotlib"]

pack = find_packages()

setup(name='structuredUMI',
        version=0.1,
        description='Python scripts for simulating structured barcode interactions',
        packages=pack,
        author='Tobias Osterlund',
        author_email='tobias.osterlund@gu.se',
        install_requires = install_requires,
        include_package_data=True,
        classifiers=['Topic :: Scientific/Engineering :: Bio-Informatics'],
        scripts=['simulation_structured_umi.py',
                'simulation_umi_design_1-7.py',
                'plot_simulation_results.py'],
        zip_safe=False)
