from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import WordWithContext
from .translate.translate import query_dictionary, translate_and_define
from django.conf import settings
from rest_framework.decorators import api_view
import json

def index(_):
    return HttpResponse('Home Page.')

def word_with_context_view(request):
    filename = 'vocab/data/translation_data.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'translations': []}
    translations = data['translations']

    if request.method == 'POST':
        form = WordWithContext(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            context = form.cleaned_data['context']
            if (settings.TESTING == False):
                # API call to PONS dictionary/translation
                translation_definition = translate_and_define(word, context)
                translation_definition_json = json.loads(translation_definition)
        
                return render(request, 
                            'vocab/word_context_success.html', 
                            {
                                'word': word, 
                                'context': context, 
                                'translated_word': translation_definition_json['translated_word'],
                                'translated_context': translation_definition_json['translated_context'],
                                'word_class': translation_definition_json['word_class'],
                            }
                            )
            else:
                return render(request, 
                            'vocab/word_context_success.html', 
                            {
                                'word': word, 
                                'context': context, 
                                'translated_word': 'translated['+ word + ']',
                                'translated_context': 'translated['+ context + ']',
                                'word_class': 'word_class'
                            }
                            ) 
    else:
        form = WordWithContext()

    return render(request, 'vocab/word_context.html', {'form': form, 'translations': translations[::-1]})

def save_translation_result(request):
    if request.method == 'POST':
        # Get translations history    
        filename = 'vocab/data/translation_data.json'
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'translations': []}


        # Extracting the translation data from the POST request
        word = request.POST.get('word')
        context = request.POST.get('context')
        translated_word = request.POST.get('translated_word')
        translated_context = request.POST.get('translated_context')
        word_class = request.POST.get('word_class')
        
        # Building a dictionary to hold the data
        new_translation_data = {
            'translation_id': len(data['translations']),
            'word': word,
            'context': context,
            'translated_word': translated_word,
            'translated_context': translated_context,
            'word_class': word_class
        }
        
        # Append the new translation to the translations list
        data['translations'].append(new_translation_data)
        
        # Write the updated data back to the file with pretty formatting
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        # Redirecting back to the form page after saving
        return redirect('word_with_context_form')
    else:
        # If the request method is not POST, redirect to the form as well
        return redirect('word_with_context_form')
    
def find_translation_index(data, translation_id):
    a = (translation_id >= 0)
    b = (translation_id < len(data['translations']))
    if (translation_id >= 0) and (translation_id < len(data['translations'])):
        if data['translations'][translation_id]['translation_id'] == translation_id:
                return translation_id
        elif data['translations'][-(1 + translation_id)]['translation_id'] == translation_id:
                return len(data['translations']) -(1 + translation_id)
        
    for index, translation in enumerate(data['translations']):
        # Assuming each 'translation' is a dictionary that has an 'id' key
        if translation.get('translation_id') == translation_id:
            return index
    return -1  # Return -1 if no match is found

def update_translation(request, translation_id):
    if request.method == 'POST':
        filename = 'vocab/data/translation_data.json'
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except:
            raise "File '" + filename + " not found."

        translation_indx = find_translation_index(data, translation_id)

        if translation_indx >= 0:
            decoded_body = request.body.decode('utf-8')
            edited_translation = json.loads(decoded_body)
            data['translations'][translation_indx] = edited_translation
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        else:
            raise "Unexpected translation_id"
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'}, status=405)