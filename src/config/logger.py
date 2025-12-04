import structlog

def configure_structlog():
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            #structlog.dev.ConsoleRenderer(),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )

configure_structlog()

logger = structlog.get_logger()

def get_logger():
    return logger