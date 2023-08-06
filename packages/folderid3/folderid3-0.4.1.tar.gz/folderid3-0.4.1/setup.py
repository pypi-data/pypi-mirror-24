from setuptools import setup
setup(
  name = 'folderid3',
  packages = ['folderid3'],
  version = '0.4.1',
  description = 'A tool for quick editing od id3 tags of audio files in a folder.',
  author = 'Jaka Rizmal',
  author_email = 'jrizmal@gmail.com',
  url = 'https://github.com/jrizmal/folderid3',
  download_url = 'https://github.com/jrizmal/folderid3/archive/0.1.tar.gz',
  keywords = ['id3', 'music', 'mp3', 'tag', 'editor', 'id3 tag'],
  classifiers = [],
  install_requires=[
      'eyeD3==0.8.1',
  ],
)