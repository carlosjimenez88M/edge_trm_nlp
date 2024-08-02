from setuptools import setup, find_packages

setup(
    name='cnn_news_extractor',
    version='0.1.0',
    description='A package to extract news from CNN Español',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'html5lib',
        'pandas',
    ],
)
