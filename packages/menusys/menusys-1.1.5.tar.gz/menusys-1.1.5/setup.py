from setuptools import setup
from menusys.menusys import __version__

packages = [
    'menusys'
]

tests_require = [
    'pytest',
]

setup(
    name='menusys',
    version=__version__,
    python_requires='~=3.5',
    description='Menu system to easily create a menu in CLI',
    keywords='menu cli easy helper dictionary',
    url='https://github.com/btr1975/menusys',
    author='Benjamin P. Trachtenberg',
    author_email='e_ben_75-python@yahoo.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    test_suite='pytest',
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
