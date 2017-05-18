import requests
from io import BytesIO
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.storage import DefaultStorage
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.http import require_safe


def process_options(options):
    parameters = {}
    options = options or ''
    for pair in options.split(';'):
        key, value = pair.split(',', maxsplit=1)
        parameters[key] = value
    return parameters


@require_safe
def image_view(request, path=None, options=None):
    if not path:
        raise Http404('No path provided')

    # Grab the default storage, to build the URL
    storage = DefaultStorage()

    # Optionaly check if the file exists in the storage
    # Depending on your storage class, this might not be implemented or performs something outrageous like loading
    # the entire file into memory
    if getattr(settings, 'RSZIO_CHECK_EXISTS', False) and not storage.exists(path):
        raise Http404('Image not found in storage')

    # Get the full URL for the image
    original_url = storage.url(path)

    # Use urllip to pull out the host and path
    parsed_url = urlparse(original_url)

    # Build the URL
    url = 'https://rsz.io/{host}{path}'.format(
        host=parsed_url.hostname,
        path=parsed_url.path,
    )

    # Build the rsz.io parameters
    try:
        parameters = process_options(options)
    except:
        # KISS: if invalid parameters are passed, raise a 404
        raise Http404('Invalid rsz.io options')

    # Grab the image
    rszio_response = requests.get(url, parameters)

    # Return
    buffer_image = BytesIO(rszio_response.content)
    buffer_image.seek(0)
    response = HttpResponse(buffer_image, content_type=rszio_response.headers['content-type'])

    # Set cache headers
    if hasattr(settings, 'RSZIO_CACHE_CONTROL'):
        try:
            response['Cache-Control'] = 'max-age={}'.format(int(settings.RSZIO_CACHE_CONTROL))
        except:
            response['Cache-Control'] = settings.RSZIO_CACHE_CONTROL

    return response
