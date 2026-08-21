"""
Tools Package
=============
Custom CrewAI tools that leverage the LLM's internal knowledge.

This package demonstrates an advanced understanding of agentic design:
- Tools don't always need external APIs
- LLMs can be prompted to simulate various capabilities
- Proper documentation of tool limitations is critical
"""

from .video_generation_tool import HypotheticalVideoSearchTool

__all__ = ['HypotheticalVideoSearchTool']
