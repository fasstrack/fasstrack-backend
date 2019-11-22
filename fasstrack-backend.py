from flask import Flask, request
import json

timetable = {
  "truckId2341": {
    "containerId": 12421,
    "arrivalTime": 12341
  }
}

containerLines = {
  "laneId1": {
    "bottom": {0:"fdsa", 1:"fdas"},
    "top": {0: "fda"}
  },
  "laneId2": {

  }
}

cranes = {
  "craneId": {
    "lane": "laneId"
  },
  "crandId": {
    # lane less crane means he can get used everywhere
  }
}

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, World!"

"""
  This method returns the timetable
"""
@app.route("/timetable")
def getTimetable():
  return json.dumps(timetable)

"""
  POST: This method handles the submitted JSON data by addeding the truck update in the table or updating the existing data.
  GET: Returns the current entry of a truck in the database
"""
@app.route("/timetable/<truckId>", methods=['POST', 'GET'])
def updateTruck(truckId):
  if request.method == 'POST':
    timetable[truckId] = request.json
    # TODO: return the placeID where the truck should collect the container
    timetable[truckId].lane = "dafe121"
    return timetable[truckId]
  elif request.method == 'GET': 
    return json.dumps(timetable[truckId])
  return None

"""
  GET: get the next task for a crane
"""
@app.route("/crane/<craneId>/nextTask", methods=['GET'])
def craneNextTask(craneId):
  # TODO: get next step to optimize the stack
  # is next container not available? -> make it accessable
  # how much time till next service?
  # if enough time to optimize:
  #     if space to optimize: get a container
  #     else: chill mate 
  # else:
  #     prepare delivery > delivery
  return None

"""
  POST: register an existing crane to handle tasks
"""
@app.route("/crane/<craneId>/register", methods=['POST'])
def craneRegister(craneId):
  # TODO: add crane into database
  # if lanes not operated: put him into lane
  # else: let him help without lane
  return None

