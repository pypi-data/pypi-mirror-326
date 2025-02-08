from setuptools import setup, find_packages

setup(
    name='cmdgen',
    version='2.0.0',
    description='Command generation tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Free Market Militia',
    author_email='FreeMarket@nostates.com',
    url='https://github.com/FreeMarketamilitia/cmdgen',
    license='MIT',
    packages=find_packages(),  # Automatically find the package folder
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # List any dependencies if required
    python_requires='>=3.6',
)
