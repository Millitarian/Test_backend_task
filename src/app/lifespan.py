import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from litestar import Litestar

from src.rabbitmq.consumer import start_consumer, stop_consumer
from src.rabbitmq.producer import broker as producer_broker

from src.config.logger import get_logger

logger = get_logger()

@asynccontextmanager
async def rabbitmq_lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    logger.info("RabbitMQ starting")

    try:
        await producer_broker.start()
        logger.info("RabbitMQ producer is connected")
    except Exception as e:
        logger.error("failed to connect RabbitMQ producer", error_type=type(e).__name__, error_message=str(e))

    app.state.rabbitmq_broker = producer_broker

    consumer_task = asyncio.create_task(start_consumer())

    await asyncio.sleep(1)

    logger.info("RabbitMQ initialized")

    yield
    
    logger.info("Stopping RabbitMQ")
    
    await stop_consumer()
    consumer_task.cancel()
    
    try:
        await consumer_task
        logger.info("RabbitMQ consumer is disabled")
    except Exception as e:
        logger.error("Error disabling consumer", error_type=type(e).__name__, error_message=str(e))

    try:
        await producer_broker.stop()
        logger.info("RabbitMQ producer is disabled")
    except Exception as e:
        logger.error("Error disabling producer", error_type=type(e).__name__, error_message=str(e))

    print("RabbitMQ stopped")