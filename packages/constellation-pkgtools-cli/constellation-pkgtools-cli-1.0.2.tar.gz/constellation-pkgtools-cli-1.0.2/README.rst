Constellation Package Tool CLI
==============================

This tool allow you to create, run and publish Constellation packages from a CLI. For more information go to the `Constellation Developer Portal <https://developer.myconstellation.io>`_.

Installation
------------

``pip install constellation-pkgtools-cli``

Usage
------------
- ``ctln create <name> [--template=<id>]``
- ``ctln update``
- ``ctln run [--server=<name>]``
- ``ctln publish --output=<directory> [--filename=<name>]``
- ``ctln publish <server_name> [--filename=<name>]``
- ``ctln pyscript list``
- ``ctln pyscript add <filepath> [--filename=<name>]``
- ``ctln pyscript new <filename> [<item_template_name>]``
- ``ctln pyscript remove <filename>``
- ``ctln pyscript rename <old_name> <new_name>``
- ``ctln server list``
- ``ctln server (add | set) <name> --url=<url> --accesskey=<key>``
- ``ctln server (add | set) <name> --url=<url> --username=<user>``
- ``ctln server remove <name>``
- ``ctln server test <name>``
- ``ctln template list``
- ``ctln (-h | --help)``
- ``ctln (-v | --version)``