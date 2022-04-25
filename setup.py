import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="networker",
    version="0.1.0",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=["networker"],
    description=" a python package to generate and analyse protein similarity networks",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/networker/tree/ver010",
    license='GNU General Public License v3.0',
    python_requires='>=3.7',
    install_requires=[]
)