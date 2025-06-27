# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""hello 
"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""**Analyzing the Greeting**

I've successfully identified the input as a simple greeting and recognized its type. My next step involved determining the most natural and expected response, which, as anticipated, is a reciprocal greeting. I am ready to proceed with the appropriate action.


**Defining the Response**

I've refined the initial response, settling on a straightforward \"Hello!\" as a direct answer. I then decided that adding a helpful offer would be a plus, but ultimately opted for simplicity. I've concluded that \"Hello!\" is a fitting and friendly response that appropriately matches the original greeting.


"""),
                types.Part.from_text(text="""Hello! How can I help you today?"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
