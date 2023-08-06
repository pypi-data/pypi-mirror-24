# coding=utf-8
from distutils.core import setup
setup(
  name='pydeepl',
  packages=['pydeepl'],
  version='0.3',
  description='An API wrapper for deepl.com translating service.',
  author='Emilio Carrión Peñalba',
  author_email='emiliok1997@gmail.com',
  url='https://github.com/EmilioK97/pydeepl',
  keywords=['translate', 'translation', 'example'],
  classifiers=[],
  install_requires=[
    'requests>=2.18.4',
  ],
)
