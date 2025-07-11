from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Adiciona uma classe CSS a um widget de formulário.
    
    Uso:
    {{ form.field|add_class:"form-control" }}
    """
    return value.as_widget(attrs={"class": css_class})
