# app/logging_utils.py
import logging

def get_logger_factory(module_name: str):
    def get_logger() -> logging.Logger:
        return logging.getLogger(module_name)
    return get_logger
