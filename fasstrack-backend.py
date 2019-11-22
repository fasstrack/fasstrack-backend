from flask import Flask, request
import json

timetable = {
  "truckId2341": {
    "containerId": 12421,
    "arrivalTime": 12341
  }
}

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/timetable")
def getTimetable():
  return json.dumps(timetable)

@app.route("/timetable/<truckId>", methods=['POST', 'GET'])
def updateTruck(truckId):
  if request.method == 'POST':
    timetable[truckId] = request.json
    return request.json
  elif request.method == 'GET': 
    return json.dumps(timetable[truckId])
  return None