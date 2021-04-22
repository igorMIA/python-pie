import setuptools
import io

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with io.open('./src/pie/version.py', encoding='utf-8') as file:
    exec(file.read(), version)

setuptools.setup(
    name="python-pie",
    version=version['__version__'],
    author="Igor Matchenko",
    author_email="igor@matchenko.com",
    description="Parse static files such as YAML and insert in them data from environment variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['environment variables', 'deployments', 'settings', 'env', 'configurations', 'python', 'pie'],
    url="https://github.com/igorMIA/python-pie",
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
