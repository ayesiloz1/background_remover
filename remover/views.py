from django.shortcuts import render
from django.core.files.storage import default_storage
from rembg import remove
from PIL import Image
import os
from django.conf import settings

def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        # Define directories, note: No need to prefix 'media' again since MEDIA_ROOT is used automatically
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
        
        # Ensure the directories exist
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save uploaded image to the 'uploads' directory
        input_path = os.path.join(upload_dir, uploaded_image.name)
        with default_storage.open(input_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        # Open the saved image
        input_image = Image.open(input_path)

        # Remove the background
        output_image = remove(input_image)

        # Save the output image to the 'output' directory
        output_path = os.path.join(output_dir, 'output.png')
        output_image.save(output_path)
        
        # Instead of returning to the result page immediately,
        # you return the result as part of the HTML rendering:
        return render(request, 'remover/result.html', {'output_image': os.path.join('media', 'output', 'output.png')})
    
    return render(request, 'remover/upload.html')
