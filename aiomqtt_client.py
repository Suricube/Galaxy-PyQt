import aiomqtt

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
"""             QTimer.singleShot(
                0,
                lambda p=payload, t=topic: self.incoming_message(t,p)
            ) """
 
async def publish_message(self, message: dict, name: str):
    #message = line_edit.text()
    #self.errror_widget.setText("")
    #line_edit.setStyleSheet("")
    if self.client:
        await self.client.publish("ui", message)
        #QTimer.singleShot(0, line_edit.clear)
        print("Gesendet!")