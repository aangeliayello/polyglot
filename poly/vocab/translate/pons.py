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