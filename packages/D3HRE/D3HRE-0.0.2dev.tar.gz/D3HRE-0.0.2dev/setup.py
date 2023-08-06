from distutils.core import setup

setup(
    name='D3HRE',
    version='0.0.2dev',
    packages=['D3HRE','gsee.gsee', 'tests', 'demand', 'mission_utlities', 'opendap_download'],
    license='GPL-3',
    author='caoyu',
    author_email='tsaoyu@gmail.com',
    url='https://github.com/tsaoyu/D3HRE',
    download_url='https://github.com/tsaoyu/D3HRE/archive/0.0.1dev.tar.gz',
    description='Data Driven Dynamic Hybrid Renewable Energy design and simulation framework'
)
