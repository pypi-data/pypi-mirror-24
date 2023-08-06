from setuptools import setup

setup(name='dsbox-datacleaning',
      version='0.1.2',
      url='https://github.com/usc-isi-i2/dsbox-cleaning.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      description='DSBox data preprocessing tools for cleaning data',
      license='MIT',
      packages=['dsbox', 'dsbox.datapreprocessing', 'dsbox.datapreprocessing.cleaner'],
      zip_safe=False,
      install_requires=['numpy', 'pandas', 'langdetect', 'scipy', 'scikit-learn', 'python-dateutil', 'six', 'fancyimpute', 'dsbox-dataprofiling']
      )
