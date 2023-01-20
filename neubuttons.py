#!/usr/bin/python3
import json

# {
#   "x": 87,
#   "y": 63,
#   "playerInvOnly": true,
#   "anchorRight": false,
#   "anchorBottom": false,
#   "backgroundIndex": 0,
#   "command": "42",
#   "icon": "ABSORPTION"
# },


xMin = -300
xMax = 300
yMin = -300
yMax = 300
step = 10
icon ="ABSORPTION"


thing = []

for x in range(xMin, xMax, step):
    for y in range(yMin, yMax, step):
        ob = dict({
                "x": x,
                "y": y,
                "playerInvOnly": True,
                "anchorRight": False,
                "anchorBottom": False,
                "backgroundIndex": 0,
                "command": "42",
                "icon": icon
            })
        thing.append(ob)

print(json.dumps(thing))
