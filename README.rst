====================
"Pur Beurre" project
====================
**Searching for food substitution in Open Food Facts french database**

*****************
TABLE OF CONTENTS
*****************

1. `DESCRIPTION`_
2. `INSTALLATION`_
3. `USAGE`_
4. `ROADMAP`_
5. `LICENSE`_
6. `PROJECT STATUS`_

DESCRIPTION
===========
This program asks the user for choosing a food product in the database and searches for an healthy alternative.
It proposes to select a category then a food product.

Data comes from Open Food Facts (OFF) french database. The program requests the OFF search API
then inserts the retrieved json data in a local database.

The program allows the user to back up his favorite food substitution in the database to read it later.

Features
------------
I. A user would like to choose a food product in order to obtain an healthy substitution.
    I.1 Retrieve OFF data using API requests (off_json_data.py : get_json_data_from_off_api()) with the "fields" keyword
    for filtering which informations are interesting in the responses (json format).

    --> One product in json data file : fig1_

    I.2 Parse the responses stored in a json object to have all food products in one list and to delete those which do not have all the required fields
II. A user would like to back up a food product substitution in order to keep it in memory as a favorite.
III. A user would like to get back his food product substitution favorites in order to read informations without repeating the research.

INSTALLATION
============
1) Install MySQL SGDB + Modify connection parameters in config.py (DB_PARAM dict).
2) Create the database executing the pur_beurre_db_creation.sql.
3) Run the main.py

Requirements
------------
|vPython badge| |vMySQL badge|

MySQL version : 5.7
Python librairies (see requirements.txt):

* certifi==2020.12.5
* chardet==4.0.0
* idna==2.10
* mysql-connector-python==8.0.23
* pkg-resources==0.0.0
* protobuf==3.14.0
* requests==2.25.1
* six==1.15.0
* urllib3==1.26.3

USAGE
=====

.. _fig1:
.. image:: ./images/1product_OFF_search_API_response.png

ROADMAP
=======

LICENSE
=======

PROJECT STATUS
==============

.. |vPython badge| image:: https://img.shields.io/badge/python-v3.8-blue.svg
.. |vMySQL badge| image:: https://img.shields.io/badge/MySQL-v5.7-yellow

