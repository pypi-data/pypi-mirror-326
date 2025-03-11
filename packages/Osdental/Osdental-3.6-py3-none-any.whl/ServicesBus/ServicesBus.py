import asyncio
import json
from typing import List, Dict, Any
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from Utils.Message import UNEXPECTED_ERROR

class ServicesBus:

    def __init__(self, conn_str:str, queue_name:str):
        self.conn_str = conn_str
        self.queue_name = queue_name

    @staticmethod
    async def send_message(self, message: dict | str) -> None:
        """Method to send a message to the Service Bus."""
        try:
            data = json.dumps(message) if isinstance(message, dict) else message
            async with ServiceBusClient.from_connection_string(self.conn_str) as servicebus_client:
                async with servicebus_client.get_queue_sender(queue_name=self.queue_name) as sender:
                    message = ServiceBusMessage(data)
                    await sender.send_messages(message)

        except Exception as e:
            raise ValueError(f'{UNEXPECTED_ERROR}: {str(e)}')


    @staticmethod
    async def send_bulk_messages(conn_str: str, queue_name: str, messages: List[Dict[str, Any]]) -> None:
        """Method to send bulk messages to the Service Bus."""
        tasks = [
            ServicesBus.send_message(conn_str, queue_name, message)
            for message in messages
        ]
        await asyncio.gather(*tasks)