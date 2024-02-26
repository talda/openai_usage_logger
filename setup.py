from setuptools import setup, find_packages

setup(
    name='openaiCostsLogger',
    version='0.1.0',
    author='Tal Darom',
    author_email='tal.darom@gmail.com',
    description='A utility for logging OpenAI API usage and costs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourgithub/openaiCostsLogger',
    packages=find_packages(),
    install_requires=[
        'json', 'logging', 'collections'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
