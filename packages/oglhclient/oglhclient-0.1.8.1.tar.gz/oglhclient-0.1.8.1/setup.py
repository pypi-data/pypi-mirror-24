from distutils.core import setup
setup(
  name = 'oglhclient',
  packages = ['oglhclient'],
  version = '0.1.8.1',
  description = 'A client for Lighthouse API',
  author = 'Lighthouse Team',
  author_email = 'engineering@opengear.com',
  url = 'https://github.com/thiagolcmelo/oglhclient',
  download_url = 'https://github.com/thiagolcmelo/oglhclient/archive/0.1.8.tar.gz',
  keywords = ['api', 'opengear', 'lighthouse'],
  classifiers = [],
  install_requires = ['pyyaml'],
  include_package_data=True,
  package_dir={'':''},
  package_data={
    '': ['*.raml', '*.html'],
  },
)
