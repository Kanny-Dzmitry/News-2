from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# Список нежелательных слов
BAD_WORDS = ['редиска', 'дурак', 'плохой']

@register.filter(name='censor')
@stringfilter
def censor(value):
    """
    Заменяет буквы нежелательных слов на символ '*'
    """
    if not isinstance(value, str):
        raise ValueError("Фильтр цензурирования применим только к строкам")
    
    result = value
    for word in BAD_WORDS:
        # Проверяем слово с большой и маленькой буквы
        for bad_word in [word, word.capitalize()]:
            if bad_word in result:
                # Оставляем первую букву, остальные заменяем на '*'
                censored = bad_word[0] + '*' * (len(bad_word) - 1)
                result = result.replace(bad_word, censored)
    
    return result 