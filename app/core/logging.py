import logging
from contextvars import ContextVar

_event_id_ctx: ContextVar[str] = ContextVar("event_id", default="-")


def set_event_id(event_id: str) -> None:
    _event_id_ctx.set(event_id)


def get_event_id() -> str:
    return _event_id_ctx.get()


class EventIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.event_id = get_event_id()
        return True


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | eventId=%(event_id)s | %(message)s",
    )

    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(EventIdFilter())
