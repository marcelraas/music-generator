from setuptools import setup, find_packages

requirements = [
    'tensorflow>=2.0.0-rc1',
    'numpy',
    'pandas',
    'scikit-learn',
    'scipy',
    'pytest',
    'moviepy',
    'plotly',
    'matplotlib',
    'pytest',
    'simpleaudio',
    'nbstripout',
    'jupyter',
    'jupyterlab',
]


setup(
    name='music_generator',
    version='0.0.2',
    packages=find_packages(),
    install_requires=requirements
)
