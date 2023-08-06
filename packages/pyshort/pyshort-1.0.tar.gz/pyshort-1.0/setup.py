from setuptools import setup
d = 'A simple python package to generate short code via predefined code and size , also you can add extra strings .'
l_d = '''
This is a beta project . 
So don't be mean . This is a simple short code generator like !@asd for my Django project . 
I just uploaded for you guys so just go easy on this project . 
It has no dependency and uses built in modules like random and string .
'''
setup(name='pyshort',
      version='1.0',
      description=d,
      long_description=l_d,
      url='https://github.com/nishowsan/pyshort/',
      author='Adib Mohsin',
      author_email='md.nishow@gmail.com',
      license='MIT',
      packages=['pyshort'],
      zip_safe=False)
