from setuptools import setup, find_packages
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setup(
    name="networker",
    version="0.1.1",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=find_packages(),
    description=" a python package to generate and analyse protein similarity networks",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/networker",
    license='GNU General Public License v3.0',
    python_requires='>=3.7',
    install_requires=['numpy','pandas','pyvis'],
    entry_points={'console_scripts': ["networker=networker.main:main"]}
)
