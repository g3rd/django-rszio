from django import template
from django.conf import settings
from django.urls import reverse


register = template.Library()


@register.simple_tag
def image(img, **kwargs):
    if not img:
        if settings.DEBUG:
            raise ValueError('No image path defined')
        return ''

    # Convert the kwargs to an appropriate string
    options = []
    for key, value in kwargs.items():
        options.append('{key},{value}'.format(key=key, value=value))

    return reverse('rszio_image', kwargs={
        'options': ';'.join(options),
        'path': img,
    })
