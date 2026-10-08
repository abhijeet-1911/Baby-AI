from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenRouter/OpenAI client only if API key is present
_OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
client = None
if _OPENROUTER_KEY:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=_OPENROUTER_KEY
        )
    except Exception:
        client = None

# Session memory
conversation = [
    {
    "role": "system",
    "content": """
    Your name is Baby.

    You are a friendly female AI assistant.

    Keep responses short and conversational.

    Never use emojis.

    Never describe emojis.

    Never explain symbols or special characters.

    Never write text such as:
    smiley face,
    smiling face,
    heart emoji,
    wink emoji,
    laughing emoji.

    Do not use markdown.

    Do not use bullet points.

    Speak naturally like a human assistant.

    Keep answers under 3 sentences unless asked for details.
    """
}
]

def ask_baby(user_text):
    """Send the user_text to the AI backend and return a reply.

    If no API key/client is configured, return a local fallback reply.
    """
    global conversation

    # Save user message
    conversation.append({"role": "user", "content": user_text})

    # If client isn't available, return a simple fallback
    if client is None:
        reply = f"I can't reach the AI service right now. You said: {user_text}"
        conversation.append({"role": "assistant", "content": reply})
        if len(conversation) > 21:
            conversation[:] = ([conversation[0]] + conversation[-20:])
        return reply

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=conversation
        )

        reply = response.choices[0].message.content

    except Exception as e:
        # On error, provide a graceful fallback
        print("AI request failed:", repr(e))
        reply = f"Sorry, I'm having trouble connecting to the AI service. You said: {user_text}"

    # Save Baby response
    conversation.append({"role": "assistant", "content": reply})

    # Keep only recent history
    if len(conversation) > 21:
        conversation[:] = ([conversation[0]] + conversation[-20:])

    return reply