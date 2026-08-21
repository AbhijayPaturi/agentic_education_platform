"""
Slides Agent Module
===================
Presentation design and slide creation.
"""

from .agent import create_slides_agent, create_slides_creation_task
from .schemas import PresentationSlides, SlideContent

__all__ = [
    'create_slides_agent',
    'create_slides_creation_task',
    'PresentationSlides',
    'SlideContent'
]
