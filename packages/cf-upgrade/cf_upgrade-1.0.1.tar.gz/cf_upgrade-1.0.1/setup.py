from setuptools import setup

version = '1.0.1'

install_requires = [
    'click',
    'boto3',
    'tabulate',
]


setup(name='cf_upgrade',
      version=version,
      description='Trivial AWS CloudFormation updater',
      long_description=open('README.rst').read() + '\n' +
              open('CHANGES.rst').read(),
      classifiers=[
          'Intended Audience :: Developers',
          'License :: DFSG approved',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='aws cloudformation',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://github.com/curvetips/cf_upgrade',
      license='BSD',
      package_dir={'': 'src'},
      packages=[''],
      install_requires=install_requires,
      entry_points='''
      [console_scripts]
      cf-upgrade = cf_upgrade:cli
      '''
      )
