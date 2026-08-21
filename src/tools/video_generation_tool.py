"""YouTube resource discovery helper for the video curation agent.

This tool does not call an external API. Instead it guides the LLM to recommend
real, reputable creators and to produce **working YouTube search URLs** so that
learners land on live, relevant results rather than dead placeholder links.
"""

from urllib.parse import quote_plus

from crewai.tools import tool


def _youtube_search_url(query: str) -> str:
    """Build a working YouTube search URL for a query."""
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


@tool("YouTube Resource Finder")
def HypotheticalVideoSearchTool(video_topic: str) -> str:
    """Recommend educational videos and produce working YouTube search links.

    Args:
        video_topic: Lesson topic or subject for video suggestions

    Returns:
        Guidance for generating 3-5 high-quality video recommendations, each
        with a reputable channel, a copy-paste search query, and a live
        YouTube search URL that returns real results.
    """
    example_url = _youtube_search_url(f"{video_topic} tutorial explained")

    return f"""
    Recommend 3-5 high-quality, MODERN educational videos for the topic
    "{video_topic}". Prioritize current best practices and up-to-date tooling.

    For each recommendation, provide:
    - A realistic, descriptive title
    - A reputable YouTube channel/creator likely to cover it well
      (e.g., freeCodeCamp, 3Blue1Brown, Fireship, StatQuest, Andrej Karpathy,
      Traversy Media, Corey Schafer — pick ones that fit the subject)
    - A concise, copy-paste search query
    - A WORKING YouTube search URL in the exact form:
      https://www.youtube.com/results?search_query=<url-encoded-query>
      (example: {example_url})

    Do NOT invent fake /watch?v=... IDs — those lead to dead links. Always use
    search URLs so the learner reaches live, relevant results.
    """
