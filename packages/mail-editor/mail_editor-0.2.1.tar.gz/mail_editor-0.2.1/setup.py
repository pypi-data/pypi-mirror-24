import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mail_editor',
    version='0.2.1',
    license='BSD',

    # packaging
    install_requires=[
        'Django>=1.8',
        'django-choices',
        'django-ckeditor',
        'premailer',
    ],
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),

    # tests
    setup_requires=['pytest-runner'],
    tests_require=[
        'factory-boy',
        'psycopg2',
        'pytest',
        'pytest-cov',
        'pytest-django',
        'pytest-pep8',
        'pytest-pylint',
        'pytest-pythonpath',
    ],

    # metadata
    description='A Django package for email template editing',
    url='https://github.com/maykinmedia/mail_editor',
    author='Sergei Maertens, Maykin Media, Jorik Kraaikamp, Joeri Bekker',
    author_email='sergei@maykinmedia.nl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
