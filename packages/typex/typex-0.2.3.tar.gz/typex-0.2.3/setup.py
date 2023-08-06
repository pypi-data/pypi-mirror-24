from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

# Setup Tool Cheat Sheet: https://pythonhosted.org/an_example_pypi_project/setuptools.html
setup(name='typex',
      version='0.2.3',
      description='A Tool for Managing Secrets',
      long_description=readme(),
      classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.4',
      ],
      keywords='secrets versioned sensitive data',
      url='https://github.com/fusionstackio/typex',
      author='Zile Rehman',
      author_email='rehmanz@yahoo.com',
      license='MIT',
      packages=['typex'],
      include_package_data=True,
      scripts=['bin/typex'],
      test_suite='nose.collector',
      tests_require=['nose'],
      install_requires=[
          'cement',
      ],
      python_requires=">=3.5",
      zip_safe=False)