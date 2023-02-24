import openai
import time

def get_prompts(text):
    # Generate three prompts using GPT-3
    message1 = openai.Completion.create(
        engine="davinci",
        prompt=f"Complete the following sentence: '{text}'\nAI response:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    message2 = openai.Completion.create(
        engine="davinci",
        prompt=f"What would a Human say in response to '{text}'?\nResponse:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()

    message3 = openai.Completion.create(
        engine="davinci",
        prompt=f"Imagine a Human conversation about '{text}'. What would the Human respond?\nResponse:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text.strip()
    if ":" in message1:
        message1 = message1.split(":")[1].strip()
    if '\n' in message1:
        message1 = message1.split("\n", 1)[0].strip()
    if 'AI' in message1:
        message1 = message1.split("AI", 1)[0].strip()
    if ":" in message2:
        message2 = message2.split(":")[1].strip()
    if '\n' in message2:
        message2 = message2.split("\n", 1)[0].strip()
    if 'AI' in message2:
        message2 = message2.split("AI", 1)[0].strip()
    if ":" in message3:
        message3 = message3.split(":")[1].strip()
    if '\n' in message3:
        message3 = message3.split("\n", 1)[0].strip()
    if 'AI' in message3:
        message3 = message3.split("AI", 1)[0].strip()
    return message1, message2, message3, "More Options"

# Set OpenAI API key
openai.api_key = "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"
