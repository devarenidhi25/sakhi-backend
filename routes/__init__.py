from .report import router as report_router
from .severity import router as severity_router
from .chatbot import router as chatbot_router

__all__ = ["report_router", "severity_router", "chatbot_router"]
