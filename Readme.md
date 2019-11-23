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

## API:

Base URL: http://34.254.196.82:5000

### Trucks:

GET ALL: [GET] /trucks
UPDATE: [POST] /trucks/<truckId>
`curl -X POST -H "Content-Type: application/json" localhost:5000/timetable/123 -d '{"time":"1234"}'`

### TimeSlots

GET ALL: [GET] /timeSlots
