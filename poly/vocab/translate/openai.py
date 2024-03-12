from openai import OpenAI
from django.conf import settings


# OpenAI
client = OpenAI(
  api_key=settings.OPENAI_API_KEY,  # this is also the default, it can be omitted
)

def translate_and_define(word, context):
    # Translate word from German to English
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": f"What is the definition of \"{word}\" in the context of \"{context}\"? Please just fill the template json with the english translations. {{\"translated_word\": \"<translated_word>\", \"translated_context\": \"<translated_context>\", \"word_class\": \"<word_class>\"}}"
            }
        ],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response.choices[0].message.content.strip()
