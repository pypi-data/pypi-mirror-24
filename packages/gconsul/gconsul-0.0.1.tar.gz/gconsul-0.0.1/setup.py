#-*- coding:utf-8 -*-

from setuptools import setup

with open("version", "r") as f:
  version=f.readline()

requirements = [
    x.strip() for x
    in open('requirements.txt').readlines() if not x.startswith('#')]
  
setup(name='gconsul',
      version=version,
      description='gevent version for python-consul',
      author='Norman Krämer',
      author_email='kraemer.norman@gmail.com',
      install_requires=requirements,
      long_description=open('README.rst').read() + '\n',
      url="https://github.com/may-day/gconsul",
      py_modules = ['consulgevent'],
      license='MIT',
      
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
)

