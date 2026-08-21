"""
Agents Package
==============
Component-based agent modules organized by functionality.

Each agent is a self-contained component with:
- Agent definition (role, goal, backstory, tools)
- Task creation functions
- Output schemas

Available Components:
- principal: Curriculum design and strategic planning
- teacher: Lesson planning and pedagogical design
- slides: Presentation design and slide creation
- video: Educational video resource curation
- test: Assessment design and quiz creation
"""

__version__ = "0.2.0"

__all__ = ['principal', 'teacher', 'slides', 'video', 'test']
