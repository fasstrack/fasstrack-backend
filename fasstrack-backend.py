import json
import random
import threading
from flask import Flask, request
from datetime import datetime
from flask_cors import CORS

MAX_TRUCKS_PER_HOUR = 3
TOTAL_SERVING_HOURS = 16
START_HOUR = 8

truckSlots = [["truckId"+str(j*MAX_TRUCKS_PER_HOUR + i) if i<(MAX_TRUCKS_PER_HOUR-1) else None for i in range(MAX_TRUCKS_PER_HOUR)] for j in range(TOTAL_SERVING_HOURS)]



timeSlots = {}

trucks = {}

container = {
  "containerId0": {
    "x": "locationX",
    "y": "locationY"
  }
}

containerLines = {
  "slotId0": [],
  "slotId1": []
}

cranes = {
  "craneId": {
    "lane": "laneId"
  },
  "crandId": {
    # lane less crane means he can get used everywhere
  }
}

def initDay():
  now = datetime.now()
  for i in range(TOTAL_SERVING_HOURS):
    for j in range(MAX_TRUCKS_PER_HOUR):
      # create time slots
      dt = now.replace(hour=i+START_HOUR, minute=j*int(60/MAX_TRUCKS_PER_HOUR), second=0, microsecond=0).strftime('%s')
      truckId = truckSlots[i][j]
      timeSlots[dt] = truckId
      # add time slots to trucks
      if truckId:
        if truckId not in trucks.keys():
          trucks[truckId] = {"containerId":"containerId"+str(i*MAX_TRUCKS_PER_HOUR+j)}
        trucks[truckId]['timeSlot'] = dt 
        trucks[truckId]['arrivalTime'] = dt 


initDay()

def isLate(truckId):
  print("check if late")
  print(trucks[truckId]['arrivalTime'], int(trucks[truckId]['timeSlot']))
  return int(trucks[truckId]['arrivalTime']) - int(trucks[truckId]['timeSlot']) > 60/MAX_TRUCKS_PER_HOUR*60  # an hour after timeslot

def getNextTimeSlot(timeStamp=datetime.now()):
  print("getNextTimeSlot")
  now = datetime.now()
  hour = timeStamp.hour
  minuit =  int(60/timeStamp.minute) if timeStamp.minute != 0 else 0
  offset = max(hour-START_HOUR, 0)
  for i in range(16-offset):
    for j in range(MAX_TRUCKS_PER_HOUR):
      dt = now.replace(hour=i+START_HOUR+offset, minute=j*int(60/MAX_TRUCKS_PER_HOUR), second=0, microsecond=0).strftime('%s')
      if int(dt) < int(timeStamp.strftime('%s')):
        continue
      print("Try slot:"+dt +" over " + timeStamp.strftime('%s'))
      if dt in timeSlots.keys() and not timeSlots[dt]:
        return dt
  print("No time slot found after "+str(timeStamp))
  return None


def removeTruckIdFromTimeSlot(truckId, timeSlot):
  print("removeTruckFromTimeSlot "+timeSlot)
  timeSlots[timeSlot] = None

def addTruckToTimeSlot(truckId, timeSlot):
  print("addTruckToTimeSlot")
  timeSlots[timeSlot] = truckId

def updateArrivalTime(truckId, arrivalTime):
  print("updateArrivalTime")
  trucks[truckId]['arrivalTime'] = arrivalTime
  oldTimeSlot = trucks[truckId]['timeSlot']
  print(oldTimeSlot)
  if isLate(truckId):
    nextTimeSlot = getNextTimeSlot(datetime.utcfromtimestamp(int(trucks[truckId]['arrivalTime']+3600)))
    if nextTimeSlot:
      trucks[truckId]['timeSlot'] = nextTimeSlot
      removeTruckIdFromTimeSlot(truckId, oldTimeSlot)
      addTruckToTimeSlot(truckId, nextTimeSlot)
    else :
      trucks[truckId]['timeSlot'] = 0

app = Flask(__name__)
CORS(app)

@app.route("/hello")
def hello():
    return "Hello, World!"

"""
  This method returns the timetable
"""
@app.route("/timeSlots")
def getTimetable():
  return json.dumps(timeSlots)

"""
  POST: This method handles the submitted JSON data by addeding the truck update in the table or updating the existing data.
  GET: Returns the current entry of a truck in the database
"""
@app.route("/trucks/<truckId>", methods=['POST', 'GET'])
def updateTruck(truckId):
  if request.method == 'POST':
    print(request.json)
    arrivalTime = request.json['arrivalTime']
    x = request.json['x']
    y = request.json['y']

    trucks[truckId].update({"x": x, "y": y})
    updateArrivalTime(truckId, arrivalTime)
    
    # TODO: return the placeID where the truck should collect the container
    timetable[truckId]["lane"] = "dafe121"
    return json.dumps({"slotId": timetable[truckId].lane});
  elif request.method == 'GET': 
    return json.dumps(trucks[truckId])
  return None

@app.route("/trucks", methods=['GET'])
def getTrucks():
  return json.dumps(trucks)

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
  laneId = craneId["laneId"]
  nextTruck = getNextTruck(laneId)
  if inReach(nextTruck):
    return "Get container "+containers[nextTruck]
  else:
    container = findUnoptimalContainer()
    return "Move container "+ container
  nextContainer = nextContainerToDeliver()
  
  if(not isReachable(nextContainer)):
    freeContainer()
  
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

def simulateTruckChange():
  threading.Timer(5.0, simulateTruckChange).start()
  for truck in trucks.keys():
    updateArrivalTime(truck, int(trucks[truck]["arrivalTime"])+  random.randint(-100,300))

simulateTruckChange()