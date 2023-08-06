from distutils.core import setup
setup(
  name = 'amqp_broker',
  packages = ['amqp_broker'],
  version = '1.4.3',
  description = 'Python library that simplified the utilisation of a AMQP client/server',
  author = 'Nicolas Beguier',
  author_email = 'nicolas_beguier@hotmail.com',
  url = 'https://github.com/nbeguier/amqp_broker',
  download_url = 'https://github.com/nbeguier/amqp_broker/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['amqp', 'broker', 'client'],
  license='Apache',
  install_requires=[
    'pika',
  ],
  classifiers = [],
)
