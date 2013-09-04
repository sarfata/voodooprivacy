## Installing boto locally ##

`create-voodoo-vpn.py` depends on the external python module
boto. Although it's not part of the standard library, it's pretty
standard, since it's the module which Amazon recommends for
interacting with Amazon Web Services. You can install it globally with
pip doing `sudo pip install boto`.

In case you don't want to tamper with your global python install, this
directory is here only to facilitate using a python virtual
environment to install the boto locally, so that it doesn't affect the
global python installation already on your system.

You must already have virtualenv installed on your system. Then the steps are:

1. $ cd pyenv 
2. $ virtualenv --no-site-packages .
3. $ pip install -r requirements.txt
4. $ source bin/activate
5. $ cd ..

Now you can do `./create-voodoo-vpn.py`
