# Fasstrack - EIT Hack The Hamburg Harbour

This is the repo to demonstrate the Fasstrack team implementation.

Located @: http://34.254.196.82:5000/hello
 
## Getting started

```
 virtualenv env --python=python3
``` 

```
 . env/bin/active 
``` 

```
 pip install -r requirements.txt
``` 
``` 
 env FLASK_APP=fasstrack-backend.py flask run
``` 

## Curl calls:

Get Timetable:
curl -X POST -H "Content-Type: application/json" localhost:5000/timetable/123 -d '{"time":"1234"}'

Update timetable:
curl localhost:5000/timetable/123
