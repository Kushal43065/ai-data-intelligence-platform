
import os
import time
from dotenv import load_dotenv
from google import genai
from groq import Groq
from openai import OpenAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

PROMPT = """
Explain how artificial intelligence is used
in detecting fraudulent digital payments.
"""


# Check HTTP error status
def get_status_code(error):
    return getattr(error, "status_code", None)


# Retry rate-limit errors
def call_with_retry(function, retries=3):

    for attempt in range(retries):
        try:
            return function()

        except Exception as error:

            status = get_status_code(error)

            if status == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait} seconds...")
                time.sleep(wait)
                continue

            if status == 413:
                raise ValueError("INPUT_TOO_LARGE") from error

            raise

    raise RuntimeError("Rate limit retries exhausted")


# Split large text
def split_text(text, max_chars=10000):

    return [
        text[i:i + max_chars]
        for i in range(0, len(text), max_chars)
    ]


# Gemini
def gemini_call(prompt):

    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key missing")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = call_with_retry(
        lambda: client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    return response.text


# Groq
def groq_call(prompt):

    if not GROQ_API_KEY:
        raise ValueError("Groq API key missing")

    client = Groq(api_key=GROQ_API_KEY)

    response = call_with_retry(
        lambda: client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    )

    return response.choices[0].message.content


# DeepSeek
def deepseek_call(prompt):

    if not DEEPSEEK_API_KEY:
        raise ValueError("DeepSeek API key missing")

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

    response = call_with_retry(
        lambda: client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    )

    return response.choices[0].message.content


# Handle oversized input by splitting recursively
def generate_with_chunks(provider, prompt):

    try:
        return provider(prompt)

    except ValueError as error:

        if str(error) != "INPUT_TOO_LARGE":
            raise

        print("Input too large. Splitting into smaller chunks.")

        chunks = split_text(prompt)
        results = []

        for index, chunk in enumerate(chunks, 1):

            print(f"Processing chunk {index}/{len(chunks)}")

            results.append(
                generate_with_chunks(provider, chunk)
            )

        return "\n".join(results)


# Automatic provider fallback
def run_llm(prompt):

    providers = [
        ("Gemini", gemini_call),
        ("Groq", groq_call),
        ("DeepSeek", deepseek_call)
    ]

    for name, provider in providers:

        try:
            print(f"\nTrying {name}...")

            result = generate_with_chunks(provider, prompt)

            print(f"Success using {name}")

            return result

        except Exception as error:

            print(f"{name} failed: {str(error)[:250]}")

    raise RuntimeError("All LLM providers failed.")


# Main menu
if __name__ == "__main__":

    print("\nAI LLM FALLBACK SYSTEM")
    print("----------------------")
    print("1. Test Gemini")
    print("2. Test Groq")
    print("3. Test DeepSeek")
    print("4. Test Automatic Fallback")

    choice = input("\nEnter your choice (1-4): ").strip()

    try:

        if choice == "1":
            answer = generate_with_chunks(gemini_call, PROMPT)

        elif choice == "2":
            answer = generate_with_chunks(groq_call, PROMPT)

        elif choice == "3":
            answer = generate_with_chunks(deepseek_call, PROMPT)

        elif choice == "4":
            answer = run_llm(PROMPT)

        else:
            print("Invalid choice")
            raise SystemExit(1)

        print("\nFINAL ANSWER")
        print("------------")
        print(answer)

    except Exception as error:
        print("\nPROGRAM ERROR:")
        print(error)
