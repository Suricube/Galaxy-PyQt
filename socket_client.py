from pydantic import BaseModel
import aiomqtt

class SocketClient(BaseModel):
    ip: str = "localhost"
    port: int = 1883

    async def start_mqtt(self):
        async with aiomqtt.Client(
            hostname=self.ip,
            port=self.port,
            username="admin",
            password="public",
        ) as client:
            await client.subscribe("mock")
            file = open("messages/capabilities.json","r")
            msg = file.read()
            file.close()
            await self.publish_message(msg,"")

            async for message in client.messages:
                print(f"Empfangen: {message.payload.decode()}")
                payload = message.payload.decode()
                topic = message.topic.value
