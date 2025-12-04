import os
from dotenv import load_dotenv

load_dotenv()

class RabbitMQConfig():
    host: str = os.getenv("RABBITMQ_HOST")
    port: str = os.getenv("RABBITMQ_PORT")
    username: str = os.getenv("RABBITMQ_USERNAME")
    password: str = os.getenv("RABBITMQ_PASSWORD")
    virtual_host: str = "/"

    @property
    def url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/{self.virtual_host}"


rabbitmq_config = RabbitMQConfig()