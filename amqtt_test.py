import asyncio
import logging

from amqtt.client import ClientError, MQTTClient
from amqtt.mqtt.constants import QOS_1, QOS_2
from component_interface import ProcessMessage
from abc import ABC, abstractmethod
"""
This sample shows how to subscribe to different $SYS topics and how to receive incoming messages 
"""
logger = logging.getLogger(__name__)


class SocketC(ABC):
    ip: str
    port: int
    process: ProcessMessage
    def __init__(self, ip, port, process):
        self.ip = ip,
        self.port = port
        self.process = process

    @abstractmethod
    async def send(msg: str):
        pass

class SocketMqtt(SocketC):
    def __init__(self, ip, port, process):
        super().__init__(ip=ip, port=port, process=process)
        self.client = MQTTClient(config={"auto_reconnect": False})
    async def connect(self):
        await self.client.connect('mqtt://127.0.0.1:1883/')
#        await self.client.connect(f"mqtt://{self.ip}:{self.port}/")

        await self.client.subscribe(
            [
                ("mock", QOS_1),
            ],
        )
        file = open("messages/capabilities.json","r")
        msg = file.read()
        file.close()
        await self.send("ui",msg)
        #await self.send("ui","test message")
        logger.info("Subscribed")
        try:
            for _i in range(1, 10):
                if msg := await self.client.deliver_message():
                    logger.info(f"{msg.topic} >> {msg.data.decode()}")
                    self.process.process(msg.data.decode())
            await self.client.unsubscribe(["$SYS/broker/uptime", "$SYS/broker/load/#"])
            logger.info("UnSubscribed")
            await self.client.disconnect()
        except ClientError:
            logger.exception("Client exception")
    async def send(self, topic:str, msg: str):
        print(msg)
        await self.client.publish('ui', msg.encode(), qos=QOS_1)


def __main__():
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    #comps = Comps()
    client = SocketMqtt(ip="localhost",port=1883, process="comps")
    asyncio.run(client.connect())

if __name__ == "__main__":
    __main__()