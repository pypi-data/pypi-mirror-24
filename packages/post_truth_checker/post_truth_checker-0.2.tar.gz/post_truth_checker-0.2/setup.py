from setuptools import setup


def reqs():
    with open('requirements.txt') as f:
        return f.read().splitlines()


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='post_truth_checker',
      version='0.2',
      description='Checks reliability of sites',
      long_description=readme(),
      url='https://github.com/AGHPythonCourse2017/zad3-detori',
      author='Wojciech Kubaty',
      include_package_data=True,
      install_requires=reqs(),
      packages=['post_truth_checker'],
      zip_safe=False)
