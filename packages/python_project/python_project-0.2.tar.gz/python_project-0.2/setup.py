from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='python_project',
      version='0.2',
      description='Python Project Template',
      url='http://github.com/rehmanz/python_project',
      author='Zile Rehman',
      author_email='rehmanz@yahoo.com',
      license='MIT',
      packages=['python_project'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False)