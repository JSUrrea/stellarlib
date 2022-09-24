from setuptools import find_packages, setup

setup (
    name = 'stellarlib',
    packages = find_packages(include = ['stellarlib']),
    version = '1.0',
    description = "Software para el procesamiento de imágenes aéreas y espaciales",
    author = "Stellar Coders",
    license = "MIT License",
    install_requires = ['numpy', 'rasterio'],
)
