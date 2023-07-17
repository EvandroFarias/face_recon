from django.http import HttpResponseBadRequest, HttpResponse
import base64
import io
from PIL import Image
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        image_data = request.body

        # Decode base64 image data
        image_bytes = base64.b64decode(image_data)

        # Open image using PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Process the image here (e.g., save it to disk, perform image recognition, etc.)
        # You can access the image using the 'image' variable

        return HttpResponse('Image received and processed successfully!')

    return HttpResponseBadRequest('Invalid request method or no image found in the request.')
