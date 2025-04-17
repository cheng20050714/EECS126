# Installation

Our labs use Jupyter. The recommended way to install it is by installing
Anaconda, an all-in-one distribution that comes with Python, Jupyter, and many
other useful packages.

Download the installers at https://www.anaconda.com/distribution/, and follow
the instructions at https://docs.anaconda.com/anaconda/install/ to set it up.
Choose the latest version of Python 3.

One thing to note is that we want Anaconda to reside in our home directory.
However, this means that we may needs to add its bin folder to our PATH
variable.

## Installing conda environment

For each lab, we will provide a conda environment to work with that contains
all of the necessary dependencies. You can install it by running:

```
conda env create --name ee126_lab0 --file ee126_lab0.yml
```


For this lab and all the following labs, if you are having trouble getting the Jupyter notebooks to run, you can use Google Colab. All the standard libraries are pre-installed and you can look up on how to install any other libraries as you need.
