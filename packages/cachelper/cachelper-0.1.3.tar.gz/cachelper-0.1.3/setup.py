from distutils.core import setup


setup(
    name='cachelper',
    version='0.1.3',
    description='A collection of cache helpers',
    author='Satoru Logic',
    author_email='satorulogic@gmail.com',
    packages=['cachelper'],
    install_requires=[
        'Werkzeug>=0.9',
    ],
)
