from setuptools import setup, find_packages


setup(
    name='changemonitor',
    version="1.3.1",
    packages=find_packages(),
    py_modules=['changemonitor_lambda'],
    include_package_data=True,
    author_email="andrew@marpasoft.com",
    install_requires=[
    ],
)
