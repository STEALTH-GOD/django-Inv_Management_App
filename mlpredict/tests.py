# test_model.py
import torch
from pathlib import Path
import torch.serialization

try:
    model_path = Path("mlpredict/models/model.pkl")
    print(f"Loading model from {model_path.absolute()}")
    
    # Method 1: Add safe globals
    try:
        import fastai.learner
        torch.serialization.add_safe_globals(['fastai.learner.Learner'])
    except ImportError:
        print("Warning: fastai not installed, trying alternate loading method")
    
    # Method 2: Use weights_only=False (less secure, but needed for fastai models)
    model = torch.load(str(model_path), map_location=torch.device('cpu'), weights_only=False)
    
    print(f"Model loaded successfully! Type: {type(model)}")
    
    # For fastai models, you might need to access the PyTorch model differently
    if hasattr(model, 'model'):
        pytorch_model = model.model
        print(f"Underlying PyTorch model: {type(pytorch_model)}")
    else:
        pytorch_model = model
    
    # Check training mode
    if hasattr(pytorch_model, 'training'):
        print("Model is in training mode:", pytorch_model.training)
        pytorch_model.eval()
        print("Model set to eval mode")
    
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()