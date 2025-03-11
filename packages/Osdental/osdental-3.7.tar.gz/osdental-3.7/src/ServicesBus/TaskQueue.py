import os
import asyncio
from dotenv import load_dotenv
from ServicesBus.ServicesBus import ServicesBus

load_dotenv()

class TaskQueue:
    """Queue to manage tasks in order and asynchronously."""

    def __init__(self):
        self.conn_str = os.getenv('CONNECTION_STRING')
        self.queue_name = os.getenv('QUEUE')
        self.service_bus = ServicesBus(self.conn_str, self.queue_name)
        self.queue = asyncio.Queue()
        asyncio.create_task(self.process_tasks())
        
    async def enqueue(self, message: dict) -> None:
        """Add a task to the queue."""
        await self.queue.put(message)

    async def process_tasks(self) -> None:
        """Process tasks from the queue in order."""
        while True:
            message = await self.queue.get()
            try:
                await self.service_bus.send_message(message)
            except Exception as e:
                raise ValueError(f'Message queuing error: {e} | Message: {message}')
            finally:
                self.queue.task_done()