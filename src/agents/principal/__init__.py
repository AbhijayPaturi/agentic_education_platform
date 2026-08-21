"""
Principal Agent Module
=====================
High-level curriculum design and strategic planning.
"""

from .agent import create_principal_agent, create_topic_identification_task
from .schemas import CurriculumProposal, TopicProposal

__all__ = [
    'create_principal_agent',
    'create_topic_identification_task',
    'CurriculumProposal',
    'TopicProposal'
]
