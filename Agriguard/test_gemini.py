from google import genai
from google import genai


client = genai.Client()


response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain what plant disease detection means in one sentence."
)


print(response.output_text)

client = genai.Client()


response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain what plant disease detection means in one sentence."
)


print(response.output_text)