from component_interface import ProcessMessage
import json
import components
import StageXY

def do_process(process: ProcessMessage, msg: str)->None:
    process.process(msg)

class Comps:
    def __init__(self):
        self.comps: dict = {}
        self.comp_area = None

    def set_comp_area(self, comp_area):
        self.comp_area = comp_area

    def set_socket_send(self, publish):
        self.publish = publish

    def process(self,str)->None:
        print(f"in comps {str}")
        try:
            data = json.loads(str)
            msg_type = data.get("type")
            match msg_type:
                case "component":
                    name = data.get("name")
                    value = data.get("payload")
                    print(f"comp:{name} {value}")
                    if name:
                        comp = self.comps[name]
                        comp.parse_msg(value)

                case "system":
                    cmd = data.get("payload", {}).get(("cmd"))
                    match cmd:
                        case "capabilities":
                            properties = data.get("payload", {}).get("properties", [])
                            for prop in properties:
                                prop_name = prop.get("name")
                                comp_type = prop.get("type")
                                self.add_sections_by_type(prop_name, comp_type)

        except json.JSONDecodeError:
            self.errror_widget.setText("wrong json format")

    def add_sections_by_type(self, name: str, comp_type: str):
        if name in self.comps:
            return
    
        component = create_component_by_type(name, comp_type, self.publish) # comp requires publish
        self.comp_area.addWidget(component)
        self.comps[name] = component
    
def create_component_by_type(name: str, comp_type: str, client)->components.Component:
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