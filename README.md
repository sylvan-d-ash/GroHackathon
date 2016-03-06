# GroHackathon
Python Hackathon

Installation
------------
* Clone the repository
* Install Python 3 if you don't have it already
* Install Requests module for python. If you have `pip` installed then simply run: `pip install requests`, else check [here](http://docs.python-requests.org/en/master/user/install/) for installation help
* Install PostgreSQL either using pip: `pip install psycopg2` OR check [here](http://initd.org/psycopg/docs/install.html#installation) for instructions

Setup
-----
* Create a PostgreSQL database
 
Run
---
To execute this script, navigate to the root folder of this repository and execute `harvest.py` and pass start date, end date, database name, database host, database user and database password as parameters. This can be done in two ways:
```
$ chmod +x harvest.py
$ ./harvest.py --start-date=2014 --end-date=2015 --database_name=my_db --database_host=localhost --database_user=root --database_pass=root
```
OR
```
$ python harvest.py --start-date=2014 --end-date=2015 --database_name=my_db --database_host=localhost --database_user=root --database_pass=root
```
