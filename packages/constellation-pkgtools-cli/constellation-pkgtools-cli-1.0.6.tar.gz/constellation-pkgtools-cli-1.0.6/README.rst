Constellation Package Tools CLI
===============================

This tool allow you to create, run and publish Constellation packages from a CLI. For more information go to the `Constellation Developer Portal <https://developer.myconstellation.io>`_.

Installation
------------

``pip install constellation-pkgtools-cli``

Usage
------------
- ``ctln create <name> [<project_template_name>]`` : Create a new Constellation package. If not set the default project template will be used. ``ctln template list`` to view available templates.
- ``ctln update`` : update the current Constellation package with the lastest template.
- ``ctln run [--server=<name>]`` : run the current Constellation package is standalone mode or connected to the specified Constellation server.
- ``ctln publish --output=<directory> [--filename=<name>]`` : publish the current Constellation package to the specified directory.
- ``ctln publish <server_name> [--filename=<name>]`` : publish the current Constellation package to the specified Constellation server.
- ``ctln pyscript list`` : list the Python scripts register by this Package configuration.
- ``ctln pyscript add <filepath> [--filename=<name>]`` : add the specified Python file to the current Constellation package.
- ``ctln pyscript new <filename> [<item_template_name>]`` : add new Python file to the current Constellation package.
- ``ctln pyscript remove <filename>`` : remove Python file from the current Constellation package.
- ``ctln pyscript rename <old_name> <new_name>`` : rename Python file on the current Constellation package.
- ``ctln server list`` : list the Constellation Servers.
- ``ctln server (add | set) <name> --url=<url> --accesskey=<key>`` : add or update a Constellation Server by using access key.
- ``ctln server (add | set) <name> --url=<url> --username=<user>`` : add or update a Constellation Server by using username & password.
- ``ctln server remove <name>`` : remove Constellation Server.
- ``ctln server check <name>`` : check the Management API connection for the specified Constellation Server.
- ``ctln template list`` : list the available project and item templates. 
- ``ctln (-h | --help)`` : show the Constellation Package Tool CLI usage.
- ``ctln (-v | --version)`` : show the Constellation Package Tool CLI version.