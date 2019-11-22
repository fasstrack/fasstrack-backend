# Fasstrack - EIT Hack The Hamburg Harbour

This is the repo to demonstrate the Fasstrack team implementation.

## Curl calls:

Get Timetable:
curl -X POST -H "Content-Type: application/json" localhost:5000/timetable/123 -d '{"time":"1234"}'

Update timetable:
curl localhost:5000/timetable/123
