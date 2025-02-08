from setuptools import setup, find_packages

setup(
    name='asd-database',
    version='1.0.0',
    packages=find_packages(),
    description='An simple database for your projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Il Tuo Nome',
    author_email='simplerpy@gmail.com',
    url='',  # Aggiorna con il link corretto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
