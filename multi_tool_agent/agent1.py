import random
from google.adk.agents import Agent

# ---------- TOOL FUNCTIONS ----------

def collect_client_story_requirements(description: str) -> dict:
    """Collects the client's desired story details.

    Args:
        description (str): Client's explanation of how they want the story to be.

    Returns:
        dict: Status and the cleaned client description or error message.
    """
    if len(description.strip()) < 10:
        return {
            "status": "error",
            "error_message": "Description is too brief. Please provide more details."
        }
    return {
        "status": "success",
        "client_description": description.strip()
    }


def generate_five_story_options(theme: str) -> dict:
    """Generates 5 different story drafts based on a given theme.

    Args:
        theme (str): The main idea or direction to build stories around.

    Returns:
        dict: Status and list of five story drafts or error message.
    """
    if not theme.strip():
        return {
            "status": "error",
            "error_message": "No theme provided. Please give a theme to generate stories from."
        }

    # Generate more detailed story options
    story_templates = [
        f"A mystery tale about {theme} where the protagonist discovers hidden secrets in an unexpected place.",
        f"An adventure story featuring {theme} with characters who must overcome personal fears to succeed.",
        f"A romantic drama centered on {theme} exploring how relationships change under pressure.",
        f"A fantasy epic involving {theme} where magic and reality collide in surprising ways.",
        f"A coming-of-age story about {theme} following a character's journey of self-discovery."
    ]

    return {
        "status": "success",
        "stories": story_templates
    }


def match_best_story(client_description: str, stories: list) -> dict:
    """Matches the best story based on client description.

    Args:
        client_description (str): What the client wants the story to be like.
        stories (list): List of 5 generated stories.

    Returns:
        dict: Status and best matching story or error.
    """
    if not client_description or not stories:
        return {
            "status": "error",
            "error_message": "Client description or story list is missing."
        }

    # Simple keyword matching logic (you can enhance this)
    description_lower = client_description.lower()
    
    # Score each story based on keyword matches
    scores = []
    keywords = {
        'mystery': ['mystery', 'secrets', 'hidden', 'discover'],
        'adventure': ['adventure', 'journey', 'quest', 'overcome'],
        'romance': ['love', 'romantic', 'relationship', 'heart'],
        'fantasy': ['magic', 'fantasy', 'magical', 'epic'],
        'coming-of-age': ['growing', 'learning', 'discovery', 'young']
    }
    
    for i, story in enumerate(stories):
        score = 0
        story_lower = story.lower()
        
        for keyword_set in keywords.values():
            for keyword in keyword_set:
                if keyword in description_lower:
                    if keyword in story_lower:
                        score += 2
                    elif any(k in story_lower for k in keyword_set):
                        score += 1
        
        scores.append((score, i, story))
    
    # Select the highest scoring story
    best_score, best_index, selected_story = max(scores, key=lambda x: x[0])
    
    return {
        "status": "success",
        "selected_story": selected_story,
        "reason": f"Selected story {best_index + 1} based on thematic alignment (score: {best_score})"
    }


# ---------- SINGLE ORCHESTRATING AGENT ----------

story_orchestrator = Agent(
    name="StoryOrchestrator",
    model="gemini-2.0-flash",
    description="Agent that handles the complete story creation workflow: collecting requirements, generating options, and selecting the best match.",
    instruction=(
        "You are a story creation assistant that helps clients through a 3-step process:\n"
        "1. First, collect detailed story requirements from the client using collect_client_story_requirements\n"
        "2. Then, generate 5 story options based on their requirements using generate_five_story_options\n"
        "3. Finally, select the best matching story using match_best_story\n\n"
        "Always follow this sequence and provide clear feedback at each step. "
        "Ask the client to describe what kind of story they want, then guide them through the complete process."
    ),
    tools=[collect_client_story_requirements, generate_five_story_options, match_best_story],
)