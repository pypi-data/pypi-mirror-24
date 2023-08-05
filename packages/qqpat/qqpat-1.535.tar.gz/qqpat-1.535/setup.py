from setuptools import setup

setup(name='qqpat',
      version='1.535',
      description='Python Financial Performance Analysys Tool',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: Financial :: Investment',
      ],
      keywords='financial time series statistics performance analytics',
      url='http://github.com/quriquant/qq-pat',
      author='QuriQuant',
      author_email='suport@quriquant.com',
      license='MIT',
      packages=['qqpat'],
      install_requires=[
          'pandas>=0.20.0',
          'pandas-datareader>=0.4',
          'scipy',
          'seaborn>=0.6.0',
          'matplotlib>=1.5.0',
          'cvxpy>=0.3.9',
          'sklearn'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
