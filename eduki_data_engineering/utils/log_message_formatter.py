import logging
from typing import List
import os
from logging import Logger, getLogger
from logging.config import fileConfig


fileConfig("configs/logging.ini")
log: Logger = getLogger()


def log_msg_formatter(logger: logging.Logger, log_lvl: str, **kwargs: str) -> None:
    """
    Creates and logs a message.

    :param logger: the logger
    :param log_lvl: the severity level of the log, it can be info or warning or error otherwise it throws an exception
    :param kwargs: keyworded, variable-length argument list, it must contain at least the following keys:
      job: the job that logs (ex status, fuelling, bus),
      entity: the entity for the log (ex 111, 536 for the stations or caetano_002 for the bus)
      msg: the log message

    :raises: Exception in case either kwargs don't include the required keys or we have a wrong severity level.
    """
    keys: List[str] = list(kwargs.keys())
    if "entity" in keys:
        log_msg: str = f'pid: {os.getpid()} | [{kwargs["job"]}-{kwargs["entity"]}]: {kwargs["msg"]}'
    else:
        log_msg: str = f'pid: {os.getpid()} | [{kwargs["job"]}]: {kwargs["msg"]}'
    for key in keys:
        if key not in ["job", "entity", "msg"]:
            log_msg += f" | {key}: {kwargs[key]}"
    if log_lvl == "info":
        logger.info(log_msg)
    elif log_lvl == "warning":
        logger.warning(log_msg)
    elif log_lvl == "error":
        logger.error(log_msg)
    else:
        raise Exception(f'[{kwargs["job"]}-{kwargs["entity"]}]: Invalid logging level')