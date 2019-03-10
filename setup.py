import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name='doc_scanner',

    version='0.1',
    author="Neeraj Singh",

    author_email="ns28@iitbbs.ac.in",
    author_website="https://myresumeapp01.herokuapp.com/",

    description="Package to scan your doc like cam scanner",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/GrayR00t/doc_scanner",
    py_modules=['doc_scanner'],

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

    ],

)
