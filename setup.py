from setuptools import setup, find_packages

setup(
    name='edi-filetriage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-magic >= 0.4.27',
        'olefile >= 0.47',
    ],
    # Metadata
    author='Jonas Hüttinger',
    author_email='jonas.huettinger@educorvi.de',
    description='A package for examine files on a very low level for triage.',
    keywords='educorvi, edi, triage, converter',
    url='https://github.com/educorvi/edi.filetriage.git',  # Project home page
)