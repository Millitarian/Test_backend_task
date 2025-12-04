import asyncio
from faststream.rabbit import RabbitBroker

class Consumer: 
    def __init__(self):
        self.broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
        self.running = False
        
        @self.broker.subscriber("user_events")
        async def print_message(msg: str):
            print(f"\n[RabbitMQ]: {msg}")
    
    async def start(self):
        if not self.running:
            self.running = True
            asyncio.create_task(self.broker.start())
            print("RabbitMQ consumer started")
    
    async def stop(self):
        if self.running:
            await self.broker.stop()
            self.running = False
            print("RabbitMQ consumer stopped")


consumer = Consumer()

async def start_consumer():
    await consumer.start()

async def stop_consumer():
    await consumer.stop()