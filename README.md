SunnyUpload
===========

Uploads status of solar panels provided by a SMA Sunny WebBox to a website. The project consists of three parts in different git repositories:

1. SunnUpload: A program that retrieves the current status of the solar panels from the Webbox and uploads them to the SunnyBackend on your webserver. It is written in Python
2. [TODO] SunnyBackend: A backend for storing measurements in a database. This is a combination of PHP and mysql.
3. [TODO] SunnyFrontend: The frontend for visualizing the measurements on a website. The frontend is written in Javascript and heavily based on jQuery.

Setup
=====

The program has been tested in Ubuntu 12.10. Required packages are:
* python3
* python3-requests

You will have to change the configuration file in the first couple of lines to make the program work.
