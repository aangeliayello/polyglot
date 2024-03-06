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


    
