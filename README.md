Verman Lab
===================

** Verman Lab is a way to visualize the Linux Kernel in order to easily manage a system's PCI Modules. **

Current components:
-----------
* [Diff] - allows you to see differences in the kernel modules that offer PCI
 driver support.
    * allows further granularity to the device level (through aliases and readable device names)
* [Cert] - allows you to see the oldest version of RHEL that will support your hardware setup
* [PCI_IDs] - a RESTful api for the [pci.ids] file used by `lspci`

How to use:
-----------
**You can use any of the components listed above simply by clicking the links.  If you'd like to be able to use the kernel you are running, follow the instructions over at the [upload portal]**

1. On your (Linux-based) system type the following to find your running kernel version:  `uname -r`
2. Visit the [upload] portal and search for your kernel version (to see if it's already in the Verman Lab database)
    * If not, you can download the shell script on that page and upload the .tar.gz file it creates
3. Browse YouTube or another fun site for about 5 minutes.  You can click the "is my kernel uploaded yet?" button to see if your kernel has been processed and is usuable by the other tools yet.

Interested in helping make Verman Lab better?
-----------
Thanks, you rule!

**Quickstart to get Verman Lab forked and running locally**:
```
# note: if you get a permission error with any of these commands, you're probably on a mac, and you probably need to run them as sudo
# fork the repo in github and clone the repo with the command below
git clone *your_clone_URL*
cd vermanlab
# install python 2.7 if you don't have it: https://www.python.org/download/releases/2.7.8/
# install pip if you don't have it: http://pip.readthedocs.org/en/latest/installing.html
# install virtualenv with the following command if you don't have it with the command below:
pip install virtualenv
# create a virtualenv to store the packages Verman Lab uses
virtualenv vermanlab_venv
# use the virtualenv you created
source vermanlab_venv/bin/activate
# install all of the packages Verman Lab requires
python setup.py install
# cd into the Django project directory
cd wsgi/openshift
# start the server and visit localhost:8000 (or other port, just change it below)
python manage.py runserver 8000
```
will be displayed, so be sure to save it somewhere. You might want 
to pipe the output of the git push to a text file so you can grep for
the password later.

