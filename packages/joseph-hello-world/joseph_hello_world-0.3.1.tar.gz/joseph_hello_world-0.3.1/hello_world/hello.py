import logging


_LOGGER = logging.getLogger("plugin.hello")


def say_hello(name: str):
    _LOGGER.info(f"Hello {name} from a plugin!")
