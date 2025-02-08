from setuptools import setup, find_packages

setup(
    name='generator-emails',
    version='0.1.0',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    description='Generator_emails - Unique Email Address Generator 🚀',
    author='Misha',
    author_email='bobyyy239@gmail.com',
    url='https://github.com/yourusername/generator-names',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT'
)
