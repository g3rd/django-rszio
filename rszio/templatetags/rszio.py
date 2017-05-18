from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag
def image(img, **kwargs):
    # Convert the kwargs to an appropriate string
    options = []
    for key, value in kwargs.items():
        options.append('{key},{value}'.format(key=key, value=value))

    return reverse('rszio_image', kwargs={
        'options': ';'.join(options),
        'path': img,
    })
