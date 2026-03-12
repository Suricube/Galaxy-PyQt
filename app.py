import sys
import asyncio
import aiomqtt
import qasync
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel,
    QScrollArea
    )
from PyQt6.QtCore import Qt
import json
import StageXY
import components
from PyQt6.QtWidgets import QSizePolicy
from w_c_systems import SytemsClass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMQX")

        
        #Layouts
        main_layout = QVBoxLayout()
        main_second_layout = QHBoxLayout()
        main_second_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_bar_layout_main = QVBoxLayout()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_bar_layout_main.addLayout(top_bar_layout)
        left_main_layout = QVBoxLayout()
        left_main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_main_layout = QVBoxLayout()
        right_main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(top_bar_layout_main)
        main_layout.addLayout(main_second_layout)
        main_second_layout.addLayout(left_main_layout,1)
        main_second_layout.addLayout(right_main_layout,2)
        main_second_layout.addStretch()

        #base widget(all widgets inherit from it)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        #top bar
        self.top_bar_connect = QPushButton("connect")
        top_bar_layout.addWidget(self.top_bar_connect)
        self.settings_button = QPushButton("→ settings")
        self.settings_button.clicked.connect(self.toggle_settings)
        top_bar_layout.addWidget(self.settings_button)
        

        #drop down panel for settings
        self.panel_settings = QWidget()
        self.panel_layout_settings = QVBoxLayout()
        self.second_panel_layout_settings = QHBoxLayout()
        self.panel_layout_settings.addLayout(self.second_panel_layout_settings)
        self.panel_settings.setLayout(self.panel_layout_settings)
        self.panel_settings.setVisible(False)
        
        main_layout.insertWidget(1, self.panel_settings)
        
        # add to panel layout settings
        self.systems = SytemsClass()
        self.second_panel_layout_settings.addWidget(self.systems.scroll_area)
        self.second_panel_layout_settings.addWidget(self.systems.scroll_area_config)
        
        #Widgets
        self.status_label = QLabel("Getrennt")
        self.errror_widget = QLineEdit()    #for error messsages
        self.errror_widget.setReadOnly(True)
        self.errror_widget.setPlaceholderText("error message appears here")
        self.errror_widget.setStyleSheet("color: red;")
        self.recieve_widget = QLineEdit()   #all recieved messages here
        self.recieve_widget.setReadOnly(True)
        self.recieve_widget.setPlaceholderText("recieved message")
        self.dynamic_widgets = QLineEdit()
        self.dynamic_widgets = {}           #all line_edits for section
        self.dynamic_buttons = {}           #all buttons for section

        # drop down pannel
        self.toggle_button = QPushButton("→ send messages")
        self.toggle_button.clicked.connect(self.toggle_panel)
        self.panel = QWidget()
        self.panel_layout = QVBoxLayout()
        self.panel.setLayout(self.panel_layout) 
        self.panel.setVisible(False)
        self.panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding) 
        self.panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        #scroll area for components
        self.component_scroll_area = QScrollArea()
        self.component_scroll_area.setWidgetResizable(True)
        self.component_scroll_area_content = QWidget()
        self.component_scroll_area_layout = QVBoxLayout(self.component_scroll_area_content)
        self.component_scroll_area.setWidget(self.component_scroll_area_content)
        self.component_scroll_area.setWidgetResizable(True)
        self.component_scroll_area.setMaximumHeight(900)
        self.panel_layout.addWidget(self.component_scroll_area)
        
        
        #add Widgets to layout
        left_main_layout.addWidget(self.status_label)
        left_main_layout.addWidget(self.toggle_button)
        left_main_layout.addWidget(self.panel)
        right_main_layout.addWidget(self.errror_widget)
        right_main_layout.addWidget(self.recieve_widget)
        left_main_layout.addStretch()       #layout formatierung
        right_main_layout.addStretch() 


    def toggle_panel(self):
        visible = self.panel.isVisible()
        self.panel.setVisible(not visible)
        if visible:
            self.toggle_button.setText("→ send messages")
        else:
            self.toggle_button.setText("↓ send messages")

    def toggle_settings(self):
        visible = self.panel_settings.isVisible()
        self.panel_settings.setVisible(not visible)
        if visible:
            self.settings_button.setText("→ settings")
        else:
            self.settings_button.setText("↓ settings")



    def on_send_clicked(self, line_edit, name):
        loop = asyncio.get_event_loop()
        loop.create_task(self.publish_message(line_edit, name))

    async def publish_message(self, message: dict, name: str):
        #message = line_edit.text()
        #self.errror_widget.setText("")
        #line_edit.setStyleSheet("")
        if self.client:
            await self.client.publish("ui", message)
            #QTimer.singleShot(0, line_edit.clear)
            print("Gesendet!")


    def incoming_message(self, topic: str, payload: str):
        self.recieve_widget.setText(payload)
        
        try:
            data = json.loads(payload)
            msg_type = data.get("type")
            
            match msg_type:
                case "component":
                    name = data.get("name")
                    value = data.get("payload")
                    print(f"comp:{name} {value}")
                    if name:
                        comp = self.dynamic_widgets[name]
                        comp.parse_msg(value)


                case "system":
                    cmd = data.get("payload", {}).get(("cmd"))
                    properties = data.get("payload", {}).get("properties", [])
                    for prop in properties:
                        prop_name = prop.get("name")
                        comp_type = prop.get("type")
                        self.add_sections_by_type(prop_name, comp_type)
                
                

        except json.JSONDecodeError:
            self.errror_widget.setText("wrong json format")

    # add component (name, type)
    def add_sections_by_type(self, name: str, comp_type: str):
        if name in self.dynamic_widgets:
            return
    
        component = create_component_by_type(name, comp_type,self.client) # comp only require publish
        self.component_scroll_area_layout.addWidget(component)
        self.component_scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.dynamic_widgets[name] = component

    async def start_mqtt(self):
        async with aiomqtt.Client(
            hostname="localhost",
            port=1883,
            username="admin",
            password="public",
        ) as client:
            self.client = client
            self.status_label.setText("Verbunden")
            await client.subscribe("mock")
            file = open("messages/capabilities.json","r")
            msg = file.read()
            file.close()
            await self.publish_message(msg,"")

            async for message in client.messages:
                print(f"Empfangen: {message.payload.decode()}")
                payload = message.payload.decode()
                topic = message.topic.value
                QTimer.singleShot(
                    0,
                    lambda p=payload, t=topic: self.incoming_message(t,p)
                )
  

def create_component_by_type(name: str, comp_type: str, client):
    print("StageXY")
    match comp_type:
        #case "componentdo":
        #    component = ComponentDO(name, "", client)
        #case "componentao":
        #    component = ComponentAO(name, "", client)
        case "StageXY":
            component = StageXY.StageXY(name, "", client)
            print("StageXY")
        case _:
            component = components.Component(name, "", client)

    component.componenet_lable.setText(name)
    #component.comp_line_edit.setPlaceholderText("message")
    return component

async def main():
    window = MainWindow()
    window.show()
    await window.start_mqtt()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(main())