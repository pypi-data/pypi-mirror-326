import asyncio
from ServicesBus.ServicesBus import ServicesBus

class TaskQueue:
    """Queue to manage tasks in order and asynchronously."""

    def __init__(self):
        self.service_bus = ServicesBus()
        self.queue = asyncio.Queue()
        

    def start_processing(self) -> None:
        """Start processing tasks in the background."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(self.process_tasks())


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