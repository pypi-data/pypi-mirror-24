from setuptools import setup

files = ["*.css"]

setup(
  name="jpyreport",
  version="1.0.0post1",
  description="Generate single HTML report from Junit xml reports",
  author="Liubov Pitko",
  author_email="lub0vpik0@gmail.com",
  url="https://github.com/lub0v/jpyreport",
  packages=["jpyreport"],
  package_data={
    'jpyreport': ['report.js', 'style.css'],
  },
  platforms=["any"],
  license="License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
  long_description="Generate single HTML report from Junit xml reports",
  install_requires=['yattag'],
  keywords='junit html reports generation',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Programming Language :: Python :: 2',
    # 'Programming Language :: Python :: 3',
  ],
  entry_points={
    'console_scripts': [
      'jpyreport=jpyreport:main',
    ],
  },
)
