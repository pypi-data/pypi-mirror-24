from setuptools import setup

setup(name='datamodule',
      version='0.1r',
      description='Package for obtain data from my dataportal',
      long_description='A portal for work with Audio samples from hydrophones under the sea.\nData is stored on a sshed machine, and a specific format.\nThe system pretend to translate to a common .wav file, catalog, offer an user and machine friendly accessibility, for Terabyte of data.',
      url='http://neuron4web.palermo.enea.it/data/index.html',
      python_requires='>=2.7, <3',
      author='iMuttley',
      author_email='tommaso.nicosia@enea.it',
      license='MIT',
      packages=['datamodule'],
      zip_safe=False)
