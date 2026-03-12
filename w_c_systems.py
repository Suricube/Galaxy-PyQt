from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QScrollArea
    )
from clickable_line_edit import ClickableLineEdit
from PyQt6.QtCore import Qt
import request_url


class SytemsClass(QWidget):
    def __init__(self):
        super().__init__()
        #variable to hold selcted wasm 
        self.wasm_selected:str = ""
        #variable to hold start of wasm path
        self.wasm_path:str = ""
        #variable to hold selected config
        self.config_selected: str = ""
        # url widgets
        self.scroll_area = QScrollArea()
        self.scroll_area_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_area_content)
        #scroll menu for wasm config
        self.scroll_area_config = QScrollArea()
        self.scroll_area_config_content = QWidget()
        self.scroll_config_layout = QVBoxLayout(self.scroll_area_config_content)
        
        #create line edits and add to layout
        url = request_url.URL()
        tree = url.get_github_tree("https://api.github.com/repos/Suricube/Galaxy-Components/git/trees/main?recursive=1")
        blobs: dict = url.get_blobs(tree)
        self.blobs = blobs

        self.blob_line_edits_wasm = []
        for path, link in blobs.items():  
            if path[-1] == "m":
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

    def return_pressed_wasm(self):
        sender = self.sender()  #which line edit was pressed 
        msg = sender.text()
        self.wasm_selected = msg
        self.config_selected = ""
        self.wasm_path = self.slice_path_name(msg)
        for le in self.blob_line_edits_wasm:
            le.setStyleSheet("")
        sender.setStyleSheet("border: 2px solid #4a90d9;")

        #refill new config list with matching jsons
        new_line_edits = []
        for path, link in self.blobs.items():
            if path[-1] == "n" and self.slice_path_name(path) == self.wasm_path:
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