# Half-Life Physics Reference

![Gordon and Scientist](https://raw.githubusercontent.com/Matherunner/hldoc/master/source/images/gordon-scientist.jpg)

![Build status](https://github.com/Matherunner/hldoc/actions/workflows/deploy.yml/badge.svg)

This repo contains the source files for the Half-Life physics documentation hosted at **https://www.jwchong.com/hl/**.

## Building

Install python. Then first create a python `venv` folder:

    $ python -m venv venv

Activate the venv:

    $ . ./venv/bin/activate

Then install the packages:

    $ pip install -r requirements.txt

Install the node packages needed for the MathJax rendering script:

    $ npm install

To build the HTML files, run

    $ python build.py build

## Licence

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-nd/4.0/)

This work is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).
