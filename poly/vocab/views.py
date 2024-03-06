from django.shortcuts import render
from django.http import HttpResponse
from .forms import WordWithContext
from .tranlate.translate import query_dictionary, translate_and_define
from django.conf import settings
import json

def index(_):
    return HttpResponse('Home Page.')

def word_with_context_view(request):
    from django.template.loaders.app_directories import get_app_template_dirs
    print(get_app_template_dirs('templates'))

    if request.method == 'POST':
        form = WordWithContext(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            context = form.cleaned_data['context']
            
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
        form = WordWithContext()

    return render(request, 'vocab/word_context.html', {'form': form})


def save_translation_result(request):
    if request.method == 'POST':
        # Extracting the translation data from the POST request
        word = request.POST.get('word')
        context = request.POST.get('context')
        translated_word = request.POST.get('translated_word')
        translated_context = request.POST.get('translated_context')
        word_class = request.POST.get('word_class')
        
        # Building a dictionary to hold the data
        new_translation_data = {
            'word': word,
            'context': context,
            'translated_word': translated_word,
            'translated_context': translated_context,
            'word_class': word_class
        }
    
        # Define the filename (you might want to use a more unique or dynamic naming scheme)
        filename = 'vocab/data/translation_data.json'
        
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'translations': []}
        
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
