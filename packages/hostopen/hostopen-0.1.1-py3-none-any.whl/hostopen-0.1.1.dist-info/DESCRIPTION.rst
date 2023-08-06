Host Open v0.1.1
================

Synopsis
--------

When connected to a vagrant machine via ssh, this allows the user to open files and directories on the host machine without tunnelling.

This functionality is restricted to only files/directories in synced folders.

Requirements
------------
- python3
- vagrant

Setup
-----

Installation
~~~~~~~~~~~~
You can install ``hostopen`` with ``pip``

::

    pip3 install hostopen


This will give the commands: ``hostopen`` and ``hostopen-server``  

Vagrantfile configuration
~~~~~~~~~~~~~~~~~~~~~~~~~
The virtual machine needs access to the ``synced_folders`` file for this program to work. This file is located in the ``.vagrant`` directory in the same root as the Vagrantfile.  

Add a similiar line to the Vagrantfile:  
::

    config.vm.synced_folder ".vagrant/machines/default/virtualbox", "/.vagrant_info"

*This assumes the machine is named 'default' and you are using 'virtualbox'. Change where appropriate.*

SSH
~~~
::

    vagrant ssh -- -R 12355:localhost:12355

*The arbitrarily chosen default port of 12355 can be changed.*


Usage Examples
--------------
You can use ``hostopen --help`` and ``hostopen-server --help`` for usage information.

Client
~~~~~~
::

    hostopen file.py directory

Will make the server open ``file.py`` and ``directory`` if they are inside of a synced folder.

Server
~~~~~~
::

    hostopen-server subl

Filepaths received will be opened with sublime. ``subl`` can be substitued for a different program.


License
-------
| Copyright (c) Jake Treacher. All rights reserved.  
| Licensed under the `MIT`_ License.

.. _MIT: https://github.com/jaketreacher/hostopen/blob/master/LICENSE.txt

