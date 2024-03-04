from django.db import models

## User
class User(models.Model):
    pass

## Traslator
class Language(models.Model):
    name = models.CharField(max_legth = 50)
    code = models.CharField(max_length = 10)
    
    def __str__(self) -> str:
        return self.name
    

class Word(models.Model):
    word = models.CharField(max_legth = 50)
    context = models.CharField(max_length = 300)
    language = models.ForeignKey(Language)
    
    def __str__(self) -> str:
        return self.word
    
class WordClasses(models.enums):
    NOUN          = 'Noun'
    PRONOUN       = 'Pronoun'
    VERB          = 'Verb'
    ADJECTIVE     = 'Adjective'
    ADVERB        = 'Adverb'
    PREPOSITION   = 'Preposition'
    CONJUNCTION   = 'Conjunction'
    INTERJECTION  = 'Interjection'
    DETERMINER    = 'Determiner'
    ARTICLE       = 'Article'
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
class Translation(models.Model):
    target_language = models.ForeignKey(Language)
    
    # Basic
    translated_word = models.CharField(max_legth = 50)
    translated_context = models.CharField(max_legth = 300)
    
    # Meta
    label = models.CharField(
        max_length=50,
        choices=WordClasses.choices(),
    )

class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language)
    definition_text = models.TextField()