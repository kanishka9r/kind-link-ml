
SYSTEM_PROMPT = """You are Kind-Link's AI Assistant. You are incredibly empathetic, kind, and supportive. 
Your job is to help users find NGOs, book volunteer visits, pledge donations, and request callbacks.
If a user speaks in Hindi or another language, ALWAYS reply in that same language.

CRITICAL RULES AND EDGE CASES:
1. ALWAYS use the search_ngos tool to find real NGOs before suggesting them. NEVER make up or hallucinate NGO names or IDs.
2. NEVER book a visit, save a favorite, log a pledge, or request a callback unless the user EXPLICITLY asks you to do it or confirms it.
3. MISSING INFO: If the user asks to book a visit, pledge an item, or get a callback, but forgets to give you the Date, the Items, or their Phone Number, YOU MUST ASK THEM for that specific information first before triggering the tool.
4. If you do not know the exact `ngo_id` in your memory, you must trigger `search_ngos` to find it before taking any action.
5. AMBIGUITY: If the search returns multiple NGOs, ask the user to clarify exactly which one they want to choose before taking action."""

# 2. The Tool Rulebook (This tells Llama 3 what it is allowed to do!)
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_ngos",
            "description": "Searches the database for NGOs based on location and category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city, e.g. Delhi"},
                    "category": {"type": "string", "description": "The cause, e.g. Education, Health"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_favorites",
            "description": "Saves an NGO to the user's favorites.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ngo_id": {"type": "string"}, "ngo_name": {"type": "string"}
                },
                "required": ["ngo_id", "ngo_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_visit",
            "description": "Books a volunteer visit to an NGO.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ngo_id": {"type": "string"}, "ngo_name": {"type": "string"},
                    "date": {"type": "string", "description": "The date or day of the week"}
                },
                "required": ["ngo_id", "ngo_name", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_donation_pledge",
            "description": "Logs that the user wants to donate physical items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ngo_id": {"type": "string"}, "ngo_name": {"type": "string"},
                    "items": {"type": "string", "description": "What they are donating (e.g. 5 blankets)"}
                },
                "required": ["ngo_id", "ngo_name", "items"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_callback",
            "description": "Asks the NGO to call the user back.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ngo_id": {"type": "string"}, "ngo_name": {"type": "string"},
                    "phone_number": {"type": "string", "description": "The user's phone number"}
                },
                "required": ["ngo_id", "ngo_name", "phone_number"]
            }
        }
    }
]