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


#### Angular
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WordContextSerializer

class WordWithContextView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WordContextSerializer(data=request.data)
        if serializer.is_valid():
            word = serializer.validated_data['word']
            context = serializer.validated_data['context']
            # Your logic here, e.g., translation_definition
            return Response({
                'word': word,
                'context': context,
                'WordWithContextView': 'Working' # TODO: Remove this line
            })
        return Response(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        form = WordWithContext() # Your form logic for GET request
        return Response({'form': form}) # Adjust as needed