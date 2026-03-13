from PyQt6.QtWidgets import ( QPushButton,
    QVBoxLayout, QHBoxLayout, QLineEdit
)

import json
import asyncio
from pydantic import BaseModel
from components import Component
from PyQt6.QtGui import QColor

class StageXY(Component):
    def __init__(self,name,  value, mqttclient):
        super().__init__(name,  value, mqttclient)
        #Layouts
        self.first_collumn = QVBoxLayout()
        self.second_collumn = QVBoxLayout()
        self.third_collumn = QVBoxLayout()
        self.fourth_collumn = QVBoxLayout()

        self.min_max_step = QHBoxLayout()
        #Widgets
        self.mx = QPushButton()
        self.px = QPushButton()
        self.my = QPushButton()
        self.py = QPushButton()
        self.delta = QLineEdit()
        self.componenet_lable.setText(self.name)

        self.min = QLineEdit()
        self.max = QLineEdit()
        self.step = QLineEdit()

        self.x_value = QLineEdit()
        self.y_value = QLineEdit()
        self.stop_button = QPushButton("stop")
        
        #add Layouts
        self.panel_layout.addLayout(self.first_collumn)
        self.panel_layout.addLayout(self.second_collumn)
        self.panel_layout.addLayout(self.third_collumn)
        self.panel_layout.addLayout(self.fourth_collumn)

        #add widgets to layout
        self.first_collumn.addWidget(self.mx)

        self.second_collumn.addWidget(self.py)
        self.second_collumn.addWidget(self.delta)
        self.second_collumn.addWidget(self.my)

        self.third_collumn.addWidget(self.px)

        self.fourth_collumn.addWidget(self.stop_button)
        self.fourth_collumn.addLayout(self.min_max_step)
        self.min_max_step.addWidget(self.min)
        self.min_max_step.addWidget(self.max)
        self.min_max_step.addWidget(self.step)
        self.fourth_collumn.addWidget(self.x_value)
        self.fourth_collumn.addWidget(self.y_value)

        #min max x,y values
        self.xmin: float = float('-inf')
        self.xmax: float = float('inf')
        self.ymin: float = float('-inf')
        self.ymax: float = float('inf')


        #button callbacks
        #x,y axis
        self.mx.clicked.connect(lambda: self.move_rel("x", -1, self.delta.text()))
        self.px.clicked.connect(lambda: self.move_rel("x", +1, self.delta.text()))
        self.my.clicked.connect(lambda: self.move_rel("y", -1, self.delta.text()))
        self.py.clicked.connect(lambda: self.move_rel("y", +1, self.delta.text()))
        #stop
        self.stop_button.clicked.connect(self.stop_button_callback)
        #line edit callback
        self.x_value.returnPressed.connect(lambda name = "x":self.line_edit_return(self.x_value.text(), name))
        self.y_value.returnPressed.connect(lambda name = "y":self.line_edit_return(self.y_value.text(), name))
        self.x_value.textEdited.connect(lambda:self.check_bounds("x"))
        self.y_value.textEdited.connect(lambda:self.check_bounds("y"))

    def check_bounds(self, name):
        match name:
            case "x":
                text = self.x_value.text()
                vmin, vmax = self.xmin, self.xmax
                widget = self.x_value
            case "y":
                text = self.y_value.text()
                vmin, vmax = self.ymin, self.ymax
                widget = self.y_value

        try:
            value = float(text)
            in_bounds = vmin <= value <= vmax  
            widget.setStyleSheet("color: white;" if in_bounds else "color: red;")
        except ValueError:
            widget.setStyleSheet("color: red;")  
        


    def parse_msg(self, msg: dict):
        print(f"IN stage{msg}")
        properties = msg.get("properties")
        cmd = msg.get("cmd")
        print(f"in stage: {cmd}")

        match cmd:
            case "config":
                for prop in properties:
                    axis = Axis(**prop)
                    print(axis.model_dump())
                    match axis.name:
                        case "x":
                            self.mx.setText(f"-{axis.name}")
                            self.px.setText(f"+{axis.name}")
                            self.x_value.setText(str(prop.get("pos", {}).get("value", "")))
                            self.xmin = float(prop.get("pos", {}).get("min"))
                            self.xmax = float(prop.get("pos", {}).get("max"))
                            if prop.get("pos", {}).get("max") >= prop.get("pos", {}).get("value", "") >= prop.get("pos", {}).get("min"): 
                                self.x_value.setStyleSheet("color: white;")
                            else: 
                                self.x_value.setStyleSheet("color: red;")
                        case "y":
                            self.my.setText(f"-{axis.name}")
                            self.py.setText(f"+{axis.name}")
                            self.y_value.setText(str(prop.get("pos", {}).get("value", "")))
                            self.ymin = float(prop.get("pos", {}).get("min"))
                            self.ymax = float(prop.get("pos", {}).get("max"))
                            if prop.get("pos", {}).get("max") >= prop.get("pos", {}).get("value", "") >= prop.get("pos", {}).get("min"): 
                                self.y_value.setStyleSheet("color: white;")
                            else: 
                                self.y_value.setStyleSheet("color: red;")
            case "update":
                for prop in properties:
                    print(prop)
                    match prop.get("name"):
                        case "x":
                            self.x_value.setText(str(prop.get("value", "")))
                        case "y":
                            self.y_value.setText(str(prop.get("value", "")))
                    
    

    def move_rel(self, name: str, sign: int, value):
        if value == "":
            return
        match name, sign:
            case "x", -1:
                value2 = "-"+value
            case "x", 1:
                value2 = value
            case "y", -1:
                value2 = "-"+value
            case "y", 1:
                value2 = value
        
        message = {
            "cmd": "moverel",
            "properties": [
            {"name": name, "value": value2}
            ]
        }
        print(message)
        asyncio.ensure_future(self.client.publish("ui", json.dumps(message)))

    def stop_button_callback(self):
        msg = {
            "cmd": "stop",
            "properties": {}
        }
        asyncio.ensure_future(self.client.publish("ui", json.dumps(msg)))
    
    def line_edit_return(self, value, name):
        match name:
            case "x":
                if "red" in self.x_value.styleSheet():
                    return
                msg_x = {
                    "cmd": "moveabs",
                    "properties": [
                    {"name": "x","value": value},
                    ]
                }
                asyncio.ensure_future(self.client.publish("ui", json.dumps(msg_x)))
            case "y":
                if "red" in self.y_value.styleSheet():
                    return
                msg_y = {
                    "cmd": "moveabs",
                    "properties": [
                    {"name": "x","value": value},
                    ]
                }
                asyncio.ensure_future(self.client.publish("ui", json.dumps(msg_y)))
 
class Range(BaseModel):
    min: float
    max: float
    value: float
    step: float

class Axis(BaseModel):
    name: str
    pos: Range
    speed: Range
    status: str



