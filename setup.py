from setuptools import setup, find_packages

# requirements = ['torch==1.0.0',
#                 'scikit-image==0.14.1',
#                 'scikit-learn==0.20.1',
#                 'pandas==0.23.4',
#                 'matplotlib==3.0.2',
#                 'plotnine==0.5.1',
#                 'tqdm==4.28.1']

requirements = [
    'tensorflow>=2.0.0a0',
    'numpy',
    'pandas',
    'matplotlib',
    'scikit-learn',
    'scipy',
    'pytest',
    'moviepy'
]

setup(
    name='music_generator',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements
)
