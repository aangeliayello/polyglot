import openai
import requests
from django.conf import settings

def get_available_dictionaries(language):
    url = f"https://api.pons.com/v1/dictionaries?language={language}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    
def query_dictionary(search_term, dictionary="deen", source_language=None, fuzzy_match=False, include_references=False):
    url = f"https://api.pons.com/v1/dictionary?q={search_term}&l={dictionary}"
    if source_language:
        url += f"&in={source_language}"
    if fuzzy_match:
        url += "&fm=1"
    if include_references:
        url += "&ref=true"
    
    headers = {"X-Secret": settings.PONS_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    


from openai import OpenAI
from django.conf import settings

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
