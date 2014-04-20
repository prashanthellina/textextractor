from setuptools import setup, find_packages

setup(
    name="textextractor",
    version='0.1',
    description="Extracts relevant body of text from HTML page content.",
    keywords='textextractor',
    author='Prashanth Ellina',
    author_email="Use the github issues",
    url="https://github.com/prashanthellina/textextractor",
    license='MIT License',
    install_requires=[
        'lxml',
    ],
    package_dir={'textextractor': 'textextractor'},
    packages=find_packages('.'),
    include_package_data=True,

    entry_points = {
        'console_scripts': ['textextractor = textextractor:textextractor_command'],
    },
)
