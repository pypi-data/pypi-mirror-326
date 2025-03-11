from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scooterbot_agent',
    version='1.0.0',
    description='Scooterbot Agent',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Jimming Cheng',
    author_email='jimming@gmail.com',
    packages=['scooterbot_agent'],
    install_requires=[
        'openai',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
