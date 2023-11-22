from setuptools import find_namespace_packages, setup

setup(
    name='folder-cleaner',
    version='1.0',
    description='Script to sort out various stuff in the folder',
    url='https://github.com/andrii-trebukh/goit_python_core_hw07',
    author='Andrii Trebukh',
    author_email='andrew.trebukh@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=[],
    # long_description="Some long desctiption",
    # long_description_content_type="text/x-rst",
    entry_points={
        'console_scripts': [
            'clean_folder = clean_folder.clean_folder:main'
        ]
    },
    # include_package_data=True
)