import os
import setuptools


def read(fname):
    return open(
        os.path.join(os.path.dirname(__file__), fname), encoding="utf-8"
        ).read()


setuptools.setup(
    name='sarcharts',
    version='0.0.0',
    setup_requires=['Jinja2'],
    scripts=['sarcharts/bin/__init__.py'],
    entry_points={
        'console_scripts': ['sarcharts=sarcharts.bin:main']
        },
    packages=setuptools.find_packages(),
    package_data={
        'sarcharts.conf': ['*'],
        'sarcharts.html.css': ['*'],
        'sarcharts.html.img': ['*'],
        'sarcharts.html.js': ['*'],
        'sarcharts.templates': ['*'],
    },
    license='GPLv3',
    author='Pablo Fernández Rodríguez',
    url='https://github.com/pafernanr/sarcharts',
    keywords='sysstat sar sadf',
    description="""
        SarCharts gets sysstat files from provided sarfilespaths
        and generates dynamic HTML Charts.""",
    long_description_content_type='text/markdown',
    long_description=read("README.md"),
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    )
