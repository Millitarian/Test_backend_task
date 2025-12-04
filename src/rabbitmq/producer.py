from datetime import datetime
from typing import Optional
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from pydantic import BaseModel

from src.config.rabbitmq import rabbitmq_config
from src.config.logger import get_logger

logger = get_logger()

class UserEvent(BaseModel):
    event_type: str
    user_id: int
    trace_id: str


broker = RabbitBroker(url=rabbitmq_config.url)

app = FastStream(broker)

async def publish_user_event(event: UserEvent):
    try:
        await broker.publish(
            message=event.model_dump_json(),
            queue=RabbitQueue("user_events"),
        )
        logger.info("The event has been published", event_type=event.event_type ,user_id=event.user_id)
    except Exception as e:
        logger.error("Error publishing event", error_type=type(e).__name__, error_message=str(e))