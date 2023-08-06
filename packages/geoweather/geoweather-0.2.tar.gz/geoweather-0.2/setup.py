from setuptools import setup

setup(name='geoweather',
      version='0.2',
      description='Useful weather functions',
      url='http://github.com/nanodan/geoweather',
      author='Daniel J. Lewis',
      license='MIT',
      packages=['geoweather'],
      zip_safe=False,
      requires=['numpy','matplotlib']
)