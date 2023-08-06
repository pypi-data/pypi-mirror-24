from setuptools import setup

package = 'teasysnmp'
version = '0.1'

setup(name=package,
      version=version,
      description="Extended easysnmp with helpers to work with snmp tables",
      license="MIT",
      author="The Binary",
      author_email="binary4bytes@gmail.com",
      url='https://github.com/thebinary/teasysnmp',
      packages=["teasysnmp"],
      install_requires=[
          "easysnmp"
      ])
