"""
Video Agent Module
==================
Educational video resource curation.
"""

from .agent import create_video_agent, create_video_generation_task
from .schemas import VideoResources, VideoResource

__all__ = [
    'create_video_agent',
    'create_video_generation_task',
    'VideoResources',
    'VideoResource'
]
