from django import template

register = template.Library()


@register.filter
def verbose_name(model):
    return model._meta.verbose_name


@register.filter
def verbose_name_plural(model):
    return model._meta.verbose_name_plural


@register.filter
def class_name(model):
    return model.__class__.__name__
