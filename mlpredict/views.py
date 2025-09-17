import json
import tempfile
from django.http import JsonResponse
from django.apps import apps
from fastai.vision.all import PILImage
from PIL import Image
import io
import logging
import traceback

logger = logging.getLogger(__name__)

# Remove @csrf_exempt - we'll handle CSRF in the frontend
def predict(request):
    if request.method != 'POST' or 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    try:
        # Get the model
        app_config = apps.get_app_config('mlpredict')
        model = app_config.model
        
        if model is None:
            logger.error("ML model not loaded")
            return JsonResponse({"error": "ML model not loaded"}, status=500)
        
        # Get the uploaded image
        image_file = request.FILES['image']
        
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
            temp_path = temp.name
            for chunk in image_file.chunks():
                temp.write(chunk)
        
        # Log progress for debugging
        logger.debug(f"Image saved to {temp_path}")
        
        # Load the image with fastai
        img = PILImage.create(temp_path)
        
        # Make the prediction
        logger.debug("Making prediction")
        pred_class, pred_idx, probabilities = model.predict(img)
        
        # Get confidence score
        confidence = float(probabilities[pred_idx])
        
        logger.debug(f"Predicted class: {pred_class}, confidence: {confidence}")
        
        # Return the prediction
        return JsonResponse({
            'category': str(pred_class),
            'confidence': confidence
        })
        
    except Exception as e:
        logger.error(f"Error in predict view: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)
    
    finally:
        # Clean up temporary file
        import os
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)