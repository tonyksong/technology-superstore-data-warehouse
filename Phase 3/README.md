# CS 6400 Database Project Phase 3

## S&E’s Technology Superstore Data Warehouse Implementation
- Semester: Spring 2019<br>
- Team: 07

## Application Components
- this is a simple 2-tier application
- the backend is implemented in mySQL. Two implementations have been tested:
    - online hosted database 
    - offline (local) database hosted on a LAMP (MAMP or WAMP) stack.
    - option to toggle between both types is built into the code.
- the front-end and middleware logic is baked into Flask, which is a Python web front end. It also has been implemented via two methods:
    - online version on heroku.
    - offline version (run from command line or from IDE)
   
Details for both these methods are availabe below.
        
## How to set up development environment


Set up virtual environment:
```
knail1s-MBP.home [6400Spring19Team07]$ cd "Phase 3"
knail1s-MBP.home [Phase 3]$
knail1s-MBP.home [Phase 3]$ python3.7 -m venv venv
```

Activate virtual environment:
```
knail1s-MBP.home [Phase 3]$ . venv/bin/activate
(venv) knail1s-MBP.home [Phase 3]$
```

Install all requirements:
```
(venv) knail1s-MBP.home [Phase 3]$ pip install -r requirements.txt
```

Note: we purposely don't upload the virtual env directory to git. You are required to create a fresh venv/ locally.

## How to run (in dev environment)

```
(venv) knail1s-MBP.home [Phase 3]$ export FLASK_APP=dbtest.py
(venv) knail1s-MBP.home [Phase 3]$ flask run
 * Serving Flask app "dbtest.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

For tips set up and run this in Pycharm, please check out this [link](https://www.youtube.com/watch?v=bZUokrYanFM&feature=youtu.be)


## Running system online (Primary approach)

- Database: We have hosted our databased on magenta.myhosted.com website which provides a paid mysql service
    - recommended systems to create and populate the database are mysql workbench from Oracle
- Front-end: for the front-end we are using free online services from Heroku.
    - we have integrated this github repo such that a change (merge, push etc) triggers an automated build in heroko and deploy to this end point.

## Running system offline (Backup approach)
- by simply updating `mydbconfig.py` you can specify the local data source
- we have hosted the database on a LAMP or MAMP server downloaded from bitnami, with exactly the same data and schema as the online version.
- for running the front-end, we do it directly through PyCharm, or from the CLI. the steps are listed above in the "How to run (in dev environment)" section.


## Authors

* **Omer Ansari**
* **Kevin Elmer**
* **Richard Levine**
* **Anthony Song**


## Bibliography
- https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-pycharm
- https://devcenter.heroku.com/articles/github-integration

