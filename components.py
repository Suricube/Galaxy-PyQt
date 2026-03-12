from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel
)
import json
import sections
import asyncio
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import Qt

class Component(QWidget):
    def __init__(self, name, value, mqttclient):
        super().__init__()
        
        self.client = mqttclient
        self.name = name

        #mainlayout
        self.componenet_layout = QVBoxLayout()
        self.componenet_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.componenet_layout)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        self.setMaximumWidth(300)

        #top row widgets
        self.componenet_lable = QLabel(name)
        self.comp_button = QPushButton("⮕")
        self.comp_button.setStyleSheet("""
                                        QPushButton {
                                        background-color: transparent;
                                        border: none;
                                        color: white;
                                        }
                                        QPushButton:hover {
                                        color: lightgray;
                                        }
                                        QPushButton:pressed {
                                        color: gray;
                                        }
                                    """)
        self.topRow = QHBoxLayout()
        self.topRow.addWidget(self.componenet_lable)
        self.topRow.addWidget(self.comp_button)
        #add top row to component layout
        self.componenet_layout.addLayout(self.topRow)

        #drop down panel
        self.panel = QWidget()
        self.panel_layout = QHBoxLayout()
        self.panel.setLayout(self.panel_layout) 
        self.panel.setVisible(False)
        self.panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum) 
        self.componenet_layout.addWidget(self.panel)
        #self.componenet_layout.addStretch()
        self.comp_button.clicked.connect(self.toggle_panel)
        self.request_config()
        
        
    def toggle_panel(self):
        visible = self.panel.isVisible()
        self.panel.setVisible(not visible)
        if visible:
            self.comp_button.setText("⮕")
        else:
            self.comp_button.setText("⬇")  

    def request_config(self):
        msg =    { "type":"component",
            "name":self.name,
            "payload":{
            "cmd":"getconfig",
            "properties": {}
            }
        }
        self.send_msg(json.dumps(msg))

    def parse_msg(self, msg: dict): # msg = {"cmd":"set", "properties":{}}
        print("in comp")
        self.comp_line_edit.setText(str(msg))
        #cmd = msg.get("cmd")
        # match cmd
        #   case "set": 
    
    def send_msg(self, msg: str):
#        payload = json.dumps({"name": self.name, "value": msg})
        print(f"send: {msg}")
        loop = asyncio.get_event_loop()
        loop.create_task(self.client.publish("ui", msg))
   

#class ComponentAO(Component):
#    def __init__(self, name, value, client):
#        super().__init__(name, value, client)
#
#        self.sections = sections.SecStack[sections.SecDO]()
#
#        self.comp_line_edit_yl = QLineEdit()
#        self.comp_line_edit_yl.setPlaceholderText("yl")
#        self.comp_line_edit_yr = QLineEdit()
#        self.comp_line_edit_yr.setPlaceholderText("yr")
#        self.comp_line_edit_dl = QLineEdit()
#        self.comp_line_edit_dl.setPlaceholderText("dl")
#        self.comp_line_edit_dr = QLineEdit()
#        self.comp_line_edit_dr.setPlaceholderText("dr")
#
#        self.componenet_layout.addWidget(self.comp_line_edit_yl)
#        self.componenet_layout.addWidget(self.comp_line_edit_yr)
#        self.componenet_layout.addWidget(self.comp_line_edit_dl)
#        self.componenet_layout.addWidget(self.comp_line_edit_dr)

        

#class ComponentDO(Component):
#    def __init__(self, name, value, client):
#        super().__init__(name, value, client)
#        self.comp_line_edit_duration = QLineEdit()
#        self.comp_line_edit_duration.setPlaceholderText("duration")
#        self.comp_line_edit_units = QLineEdit()
#        self.comp_line_edit_units.setPlaceholderText("units")
#
#        self.componenet_layout.addWidget(self.comp_line_edit_duration)
#        self.componenet_layout.addWidget(self.comp_line_edit_units)



