Verman Lab
===================
## [Please, please, please report any issues you have with Verman Lab here]

** Verman Lab is a way to visualize the Linux Kernel in order to easily manage a system's PCI Modules. **

Current components:
-----------
* [Cat_PCI] - a way to see the Kernel Versions (uploaded to the database) that support the hardware you are currently running on your system
* [Diff] - allows you to see differences in the kernel modules that offer PCI
 driver support.
    * allows further granularity to the device level (through aliases and readable device names)
* [LCD_PCI] - allows you to see the oldest version of RHEL that will support your hardware setup
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

License
----

Todo: GPL

This git repository helps you get up and running quickly w/ a Django
installation on OpenShift.  The Django project name used in this repo
is 'openshift' but you can feel free to change it.  Right now the
backend is sqlite3 and the database runtime is found in
`$OPENSHIFT_DATA_DIR/sqlite3.db`.

Before you push this app for the first time, you will need to change
the [Django admin password](#admin-user-name-and-password).
Then, when you first push this
application to the cloud instance, the sqlite database is copied from
`wsgi/openshift/sqlite3.db` with your newly changed login
credentials. Other than the password change, this is the stock
database that is created when `python manage.py syncdb` is run with
only the admin app installed.

On subsequent pushes, a `python manage.py syncdb` is executed to make
sure that any models you added are created in the DB.  If you do
anything that requires an alter table, you could add the alter
statements in `GIT_ROOT/.openshift/action_hooks/alter.sql` and then use
`GIT_ROOT/.openshift/action_hooks/deploy` to execute that script (make
sure to back up your database w/ `rhc app snapshot save` first :) )

You can also turn on the DEBUG mode for Django application using the
`rhc env set DEBUG=True --app APP_NAME`. If you do this, you'll get
nicely formatted error pages in browser for HTTP 500 errors.

Do not forget to turn this environment variable off and fully restart
the application when you finish:

```
$ rhc env unset DEBUG
$ rhc app stop && rhc app start
```

Running on OpenShift
--------------------

Create an account at https://www.openshift.com

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc
    rhc setup

Create a python application

    rhc app create django python-2.6

Add this upstream repo

    cd django
    git remote add upstream -m master git://github.com/openshift/django-example.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

Here, the [admin user name and password will be displayed](#admin-user-name-and-password), so pay
special attention.
	
That's it. You can now checkout your application at:

    http://django-$yournamespace.rhcloud.com

Admin user name and password
----------------------------
As the `git push` output scrolls by, keep an eye out for a
line of output that starts with `Django application credentials: `. This line
contains the generated admin password that you will need to begin
administering your Django app. This is the only time the password
will be displayed, so be sure to save it somewhere. You might want 
to pipe the output of the git push to a text file so you can grep for
the password later.

