import asyncio
import aiomqtt
import json
import app



async def handle_message(data: dict, publish_callback):
    cmd = data.get("cmd")
    config_msg:json  = json.dumps({
    "type":"component",
    "name":"stage",
    "payload":{
  "cmd": "config",
  "properties": [
    {
      "name": "x",
      "axistype": "linear",
      "pos": {"value": 0,"min": -100,"max": 100,"step": 0.1},
      "speed": {"value": 100,"min": 0,"max": 1000,"step": 1},
      "status": "initilizing"
    },
    {
      "name": "y",
      "axistype": "linear",
      "pos": {"value": 1011,"min": -100,"max": 100,"step": 0.1},
      "speed": {"value": 100,"min": 0,"max": 1000,"step": 1},
      "status": "initilizing"
    }
  ]
}

})
    if cmd == "getconfig":
            publish_callback("config", config_msg)
    else: 
        return
