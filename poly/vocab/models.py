from django.db import models

## User
class User(models.Model):
    pass

## Traslator
class Language(models.Model):
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 10)
    
    def __str__(self) -> str:
        return self.name
    

class Word(models.Model):
    word = models.CharField(max_length = 50)
    context = models.CharField(max_length = 300)
    language = models.ForeignKey(Language, on_delete = models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.word
    
class WordClasses(models.TextChoices):
    NOUN = 'Noun', 'Noun'
    PRONOUN = 'Pronoun', 'Pronoun'
    VERB = 'Verb', 'Verb'
    ADJECTIVE = 'Adjective', 'Adjective'
    ADVERB = 'Adverb', 'Adverb'
    PREPOSITION = 'Preposition', 'Preposition'
    CONJUNCTION = 'Conjunction', 'Conjunction'
    INTERJECTION = 'Interjection', 'Interjection'
    DETERMINER = 'Determiner', 'Determiner'
    ARTICLE = 'Article', 'Article'
    
class Translation(models.Model):
    target_language = models.ForeignKey(Language, on_delete = models.DO_NOTHING)
    
    # Basic
    translated_word = models.CharField(max_length = 50)
    translated_context = models.CharField(max_length = 300)
    
    # Meta
    label = models.CharField(
        max_length=50,
        choices=WordClasses.choices,
    )

class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE)
    definition_text = models.TextField()