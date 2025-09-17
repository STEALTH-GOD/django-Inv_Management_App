from django.apps import AppConfig
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

class MlpredictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mlpredict'
    model = None

    def ready(self):
        # Avoid loading model twice in development (when using auto-reloader)
        if os.environ.get('RUN_MAIN') == 'true' or not os.environ.get('RUN_MAIN'):
            try:
                from fastai.vision.all import load_learner
                model_path = Path(__file__).parent / 'models' / 'kitchen_classifier.pkl'
                
                if not model_path.exists():
                    logger.error(f"Model file not found at {model_path}")
                    return
                
                logger.info(f"Loading model from {model_path}")
                self.__class__.model = load_learner(model_path)
                logger.info("Kitchen classifier model loaded successfully!")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                import traceback
                logger.error(traceback.format_exc())