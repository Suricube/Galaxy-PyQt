from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QScrollArea, QPushButton, QHBoxLayout,
    QLineEdit
    )
from clickable_line_edit import ClickableLineEdit
from PyQt6.QtCore import Qt
import request_url
import json
import asyncio

class SytemsClass(QWidget):
    def __init__(self, publish):
        super().__init__()
        self.publish = publish
        #variable to hold selcted wasm 
        self.wasm_selected:str = ""
        #variable to hold start of wasm path
        self.wasm_path:str = ""
        #variable to hold wasm url
        self.wasm_url = ""
        #variable to hold selected config
        self.config_selected: str = ""
        #variable to hold config url
        self.config_url = ""
        # url widgets
        self.scroll_area = QScrollArea()
        self.scroll_area_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_area_content)

        #scroll menu for wasm config
        self.scroll_area_config = QScrollArea()
        self.scroll_area_config_content = QWidget()
        self.scroll_config_layout = QVBoxLayout(self.scroll_area_config_content)

        #drop down panel for settings
        self.panel_settings = QWidget()
        self.panel_layout_settings = QVBoxLayout()
        self.second_panel_layout_settings = QHBoxLayout()
        self.panel_layout_settings_select = QVBoxLayout()
        self.panel_layout_settings.addLayout(self.second_panel_layout_settings)
        self.panel_settings.setLayout(self.panel_layout_settings)
        self.panel_settings.setVisible(False)
        self.second_panel_layout_settings.addWidget(self.scroll_area)
        self.second_panel_layout_settings.addWidget(self.scroll_area_config)
        

        #create line edits and add to layout
        url = request_url.URL()
        url.set_token()
        tree = url.get_github_tree(url="https://api.github.com/repos/Suricube/Galaxy-Components/git/trees/main?recursive=1")
        blobs: dict = url.get_blobs(tree)
        self.blobs = blobs

        self.blob_line_edits_wasm = []
        for path, url in blobs.items():  
            if path[-1] == "m":
                self.wasm_url = url
                self.scroll_line_edit_wasm =  ClickableLineEdit(path)
                self.blob_line_edits_wasm.append(self.scroll_line_edit_wasm)
                self.scroll_layout.addWidget(self.scroll_line_edit_wasm)
        self.blob_line_edits_json = []
        for line_edit_wasm in self.blob_line_edits_wasm:
            line_edit_wasm.setReadOnly(True)
            line_edit_wasm.clicked.connect(self.return_pressed_wasm)

        # configure scroll area
        self.scroll_area.setWidget(self.scroll_area_content)
        #self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(300, 200)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    
        # configure scroll area for wasm config
        self.scroll_area_config.setWidget(self.scroll_area_config_content)
        self.scroll_area_config.setFixedSize(300, 200)

        #actor name id line edit
        self.actor_name_id = QLineEdit()
        self.actor_name_id.setPlaceholderText("enter actor name id")
        self.second_panel_layout_settings.addWidget(self.actor_name_id)

        #button for applying systems
        self.apply_systems = QPushButton("apply")
        self.apply_systems.clicked.connect(self.apply_systems_button)
        self.second_panel_layout_settings.addWidget(self.apply_systems)

        #settings button
        self.settings_button = QPushButton("→ settings")
        self.settings_button.clicked.connect(self.toggle_settings)

        #get config button 
        self.get_capabilities = QPushButton("get capabilities")
        self.get_capabilities.clicked.connect(self.get_capabilities_clicked)
        self.second_panel_layout_settings.addWidget(self.get_capabilities)


    def get_capabilities_clicked(self):
        with open("assets/get_capabilities.json", "r") as f:
            msg = json.loads(f.read())
            f.close()
            msg["type"] = "manager"
        self.send(json.dumps(msg))

    def return_pressed_wasm(self):
        sender = self.sender()  #which line edit was pressed 
        msg = sender.text()
        self.wasm_selected = msg
        self.config_selected = ""
        #self.wasm_url_selected = msg
        self.wasm_path = self.slice_path_name(msg)
        for le in self.blob_line_edits_wasm:
            le.setStyleSheet("")
        sender.setStyleSheet("border: 2px solid #4a90d9;")

        #refill new config list with matching jsons
        new_line_edits = []
        for path, url in self.blobs.items():
            if path[-1] == "n" and self.slice_path_name(path) == self.wasm_path:
                self.config_url = url
                line_edit = ClickableLineEdit(path)
                line_edit.setReadOnly(True)
                line_edit.clicked.connect(self.return_pressed_config)
                new_line_edits.append(line_edit)
                

        # discard old content
        old_widget = self.scroll_area_config.takeWidget()
        if old_widget:
            old_widget.deleteLater()

        #create new scroll layout
        self.scroll_area_config_content = QWidget()
        self.scroll_config_layout = QVBoxLayout(self.scroll_area_config_content)

        #add new widgets
        self.blob_line_edits_json = new_line_edits
        for le in self.blob_line_edits_json:
            self.scroll_config_layout.addWidget(le)

        #append new widgets to new scroll layout
        self.scroll_area_config.setWidget(self.scroll_area_config_content)
        self.scroll_area_config_content.adjustSize()

        

    def return_pressed_config(self):
        sender = self.sender()
        self.config_selected = sender.text()
        for le in self.blob_line_edits_json:
            le.setStyleSheet("")
        sender.setStyleSheet("border: 2px solid #4a90d9;")
    
    def slice_path_name(self, path: str):
        first = path.index("/")
        second = path.index("/", first + 1)
        result = path[:second]
        return result
    
    def apply_systems_button(self):
        with open("assets/comp_fromurl.json", "r") as f:
            msg = json.loads(f.read())
            f.close()
        #urls = msg.get("payload", {}).get("properties", {}).get("wasmfile_path", {}).get("from_url")
        #for key, value in urls.items():
            #match key:
                #case "wasm_url":
                #    msg["payload"]["properties"]["wasmfile_path"]["from_url"]["wasm_url"] = self.wasm_selected
                #case "config_url":
                    #msg["payload"]["properties"]["wasmfile_path"]["from_url"]["config_url"] = self.config_selected
        if self.wasm_selected:
            msg["payload"]["properties"]["wasmfile_path"]["from_url"]["wasm_url"] = self.wasm_url
        if self.config_selected:
            msg["payload"]["properties"]["wasmfile_path"]["from_url"]["config_url"] = self.config_url
        else:
            print("config or wasm selected is empty")
            return
        if self.actor_name_id.text():
            msg["payload"]["properties"]["actor_name_id"] = self.actor_name_id.text()
            self.actor_name_id.setStyleSheet("")
        else:
            self.actor_name_id.setStyleSheet("QLineEdit { border: 2px solid red; border-radius: 3px; }")
            return
        
        #self.msg_to_apply = msg
        self.actor_name_id.clear()
        self.send(json.dumps(msg))

    def send(self, msg: str):
        loop = asyncio.get_event_loop()
        loop.create_task(self.publish("ui", msg))

    def toggle_settings(self):
        visible = self.panel_settings.isVisible()
        self.panel_settings.setVisible(not visible)
        if visible:
            self.settings_button.setText("→ settings")
        else:
            self.settings_button.setText("↓ settings")