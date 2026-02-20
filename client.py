from google import genai

# Create client once
client = genai.Client(api_key="Your_API_Key")

def aiProcess(command):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=command
    )

    return response.text
