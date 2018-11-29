# Project Description

This is a small server which provides an URL shortener for users. It was created using Python and SQLite to simulate the database. Any SQL database should be able to support some thousands of simple requests per second on a good machine, so it should be sufficient for this project.

It uses the microframework Flask for REST request routing and processing definition, Gunicorn as the main Web Server Gateway Interface to provide the Flask application inside of multiple workers and Gevent to monkey patch python native methods, improving the performance of networking methods by managing coroutines and other asynchronous functionalities.

## Instalation
I used Ubuntu 18.04 to create this project.

You need python and pip to start the installation. If you don't want to use a virtual environment for your project, use python 2.x since you need to change some configurations to make it work with python 3 without creating a virtual environment. You'll also need this environment to run Locust for data load tests if you want.

Assuming that we are using python 2.x, run:
```
sudo apt-get install python2.7
sudo apt-get install python-pip
 ```

To use a virtual environment, after installing pip run:
```
pip install virtualenv    
virtualenv venvLocust    
source venvLocust/bin/activate
```

The last command will activate a virtual environment with the name used in "virtualenv" command.

Install sqlite:
```
sudo apt-get install sqlite3    
sudo apt-get install libsqlite3-dev
```

Now move to the project folder and install the other dependencies:
```
pip install -r requirements.txt
```

Here is the dump of packages installed by it:
```
-   Successfully built flask-jsonpify itsdangerous SQLAlchemy MarkupSafe
    
-   Installing collected packages: MarkupSafe, Jinja2, Werkzeug, click, itsdangerous, flask, flask-jsonpify, aniso8601, six, pytz, flask-restful, SQLAlchemy, Flask-SQLAlchemy, greenlet, gevent, gunicorn
    
-   Successfully installed Flask-SQLAlchemy-2.3.2 Jinja2-2.10 MarkupSafe-1.0 SQLAlchemy-1.2.12 Werkzeug-0.14.1 aniso8601-3.0.2 click-7.0 flask-1.0.2 flask-jsonpify-1.5.0 flask-restful-0.3.6 gevent-1.3.7 greenlet-0.4.15 gunicorn-19.9.0 itsdangerous-0.24 pytz-2018.5 six-1.11.0
```

## Database creation

Assuming that you are inside of the project folder, first you need to create the database file. Open sqlite on your terminal:
```
sqlite3 urls.db
```

Then run any query and close the program to save a new empty database file:
```
SELECT * FROM sqlite_master where type='table';
.quit
```

Finally run a small python file which I made to create the table "shortened_url" there:
```
python create_table.py
```

## Server execution

Use this command to start the server using 9 server instances and gevent to manage workloads, the gunicorn documentation recommends that you use (2 * number of CPU cores) + 1 workers:
```
gunicorn server:app --workers=9 --worker-class gevent --log-level=info
```
This REST server has two simple routes, check the following curl command examples to see how to use each route:

### Accessing shortened URLs

You can use a GET request to access shortened URLs. It will return a 404 error if the URL id doesn't exist in our database:
```
curl -i http://127.0.0.1:8000/urlId
```

### Creating shortened URLs

You can use a POST request to create shortened URLs. It will return a shortened link to it, using the auto generated identifier created by the database to create shortened URL ids for each request sent by users. I used a simple numeric system converter to transform database ids into a base-62 number to include characters for each ID returned to the user:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"url":"www.helloworld.com"}' http://127.0.0.1:8000/shorten_url
```

The database management system will handle concurrent accesses on inserting time.  Also we use a database restriction to avoid ingesting the same URL more than one time.

## (Optional) Load Testing and Server Scaling

I used a framework called Locust to test server intense use. There is a small file called *locustfile.py* in the project folder which contains a small load test definition. To start the test, activate the virtual environment created on the installation section and run this command:
```
locust --host=http://127.0.0.1:8000
```
You'll be able to start a test session accessing the URL http://127.0.0.1:8089. Check the img folder to see some test session screenshots.


I tested it in my personal notebook, which contains:
* Intel Core i7 5500u 2.40ghz;
* 8GB RAM.

I ran Locust with 1000 users and I was able to process 140 requests per second when disabling the GET requests. GET requests are dependent of  network (to redirect the user), so I got very low requests per second results (+-10RPS) when I enabled it.

Since the project is pretty simple, maybe running it on a real server machine with a real SQL database like PostgreSQL should be enough to get thousands of requests per second. The redirect part of the code should also be executed on the user's machine (when it loads the destination URL), so in real cases, the GET server response time shouldn't be so high.

If the database model becomes a bottleneck, it is easy to use a different database system, since the shortened URL data manipulation methods are isolated from the server routing handling logic. We could, for example, use a NoSQL database with a shared counter to create the URL ids. Also we could some database like Redis to work as a cache before requesting the data from the database.

Finally, while I don't have experience with that, I also believe that we could use some orchestration system like Docker Swarm to run dozens of URL shortener servers if necessary because this project was created to access the database safely in a distributed manner.



