from setuptools import setup
__version__ = '0.8'

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='msclmodeling',
      version=__version__,
      long_description=readme(),
      description='Code for modeling muscle metabolism',
      url='http://github.com/gpabhi/msclmodeling',
      author='GP Abhi',
      author_email='abhijitg@vt.edu',
      license='MIT',
      packages=['msclmodeling'],
      install_requires = [],
      zip_safe=False)