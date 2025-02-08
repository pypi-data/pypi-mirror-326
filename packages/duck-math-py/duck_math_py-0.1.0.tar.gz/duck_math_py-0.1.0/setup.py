from setuptools import setup, find_packages

setup(
    name='duck_math_py',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    include_package_data=True,
    license='MIT',
    description='A simple Python package with a module called calc.py that provides a method total(x, y).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='jduckett',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/duck_math_py',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)