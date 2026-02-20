from google import genai

# Create client once
client = genai.Client(api_key="AIzaSyDXsDSYi6bm3Xlb3fUE1FqjMM7_bl0Y3SM")

def aiProcess(command):

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=command
    )

    return response.text