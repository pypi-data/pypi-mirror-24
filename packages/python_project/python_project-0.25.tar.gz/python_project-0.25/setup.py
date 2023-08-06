from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='python_project',
      version='0.25',
      description='Python Project Template',
      long_description='A great pip packaging example',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/rehmanz/python_project',
      author='Zile Rehman',
      author_email='rehmanz@yahoo.com',
      license='MIT',
      packages=['python_project'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)