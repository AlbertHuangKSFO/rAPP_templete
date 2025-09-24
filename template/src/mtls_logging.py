import asyncio
import json
import logging
import os
import ssl
import sys
from datetime import datetime, timezone
from enum import IntEnum

import httpx

from .config import get_config

class Severity(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class _ConsoleLogger:
    def __init__(self, name: str, console_log_level=Severity.INFO) -> None:
        self.__logger = logging.getLogger(name)
        if not self.__logger.hasHandlers():
            self.__logger.setLevel(console_log_level)
            handler = logging.StreamHandler(stream=sys.stdout)
            formatter = logging.Formatter(
                fmt="[%(asctime)s.%(msecs)03d] %(name)s [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)

    def log(self, level: int, msg: str):
        self.__logger.log(level, msg)

class _MTLSLogger:
    def __init__(self, console_logger: _ConsoleLogger) -> None:
        self.console_logger = console_logger
        self.config = get_config()
        self.log_url = f'https://{self.config.get("log_endpoint")}'
        self.is_cert_available = all([
            self.config.get("ca_cert_file_path"),
            self.config.get("ca_cert_file_name"),
            self.config.get("app_cert_file_path"),
            self.config.get("app_cert"),
            self.config.get("app_key"),
        ])

        if self.is_cert_available:
            self.client = self._create_client()
            self.log_queue = asyncio.Queue()
        else:
            self.console_logger.log(Severity.WARNING, "mTLS logging certificates not fully configured. Logs will only be sent to console.")

    def _create_client(self):
        ca_cert = os.path.join(self.config["ca_cert_file_path"], self.config["ca_cert_file_name"])
        app_cert = os.path.join(self.config["app_cert_file_path"], self.config["app_cert"])
        app_key = os.path.join(self.config["app_cert_file_path"], self.config["app_key"])
        
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_cert)
        context.load_cert_chain(certfile=app_cert, keyfile=app_key)
        return httpx.AsyncClient(verify=context, timeout=10.0)

    async def sender_task(self):
        if not self.is_cert_available:
            return
        while True:
            try:
                log_item = await self.log_queue.get()
                await self.client.post(self.log_url, json=log_item)
                self.log_queue.task_done()
            except Exception as e:
                self.console_logger.log(Severity.ERROR, f"Failed to send log via mTLS: {e}")

    def _log(self, level: Severity, message: str):
        self.console_logger.log(level, message)
        if self.is_cert_available and level >= Severity.INFO: # Example: only send INFO and above
            log_item = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": level.name.lower(),
                "service_id": self.config.get("container_name"),
                "message": message,
                "version": "1.0.0",
            }
            try:
                self.log_queue.put_nowait(log_item)
            except asyncio.QueueFull:
                self.console_logger.log(Severity.WARNING, "mTLS log queue is full. Log message dropped.")

    def debug(self, message: str): self._log(Severity.DEBUG, message)
    def info(self, message: str): self._log(Severity.INFO, message)
    def warning(self, message: str): self._log(Severity.WARNING, message)
    def error(self, message: str): self._log(Severity.ERROR, message)
    def critical(self, message: str): self._log(Severity.CRITICAL, message)

console_logger = _ConsoleLogger(get_config().get("container_name"))
logger = _MTLSLogger(console_logger)