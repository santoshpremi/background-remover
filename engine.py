import numpy as np
from PIL import Image
import torch
import model
import os
import urllib.request

torch.set_num_threads(1)

# Model path
model_path = './u2netp.pth'

# Device detection - use GPU if available, otherwise CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Download model if it doesn't exist
def download_model():
    if not os.path.exists(model_path):
        print("Downloading U2-Net model...")
        url = "https://drive.usercontent.google.com/u/0/uc?id=1rbSTGKAE-MTxBYHd-51l2hMOQPT_7EPy&export=download"
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded successfully!")

# Download model on import
download_model()

# Load the model
try:
    print("Loading U2-Net model...")
    model_pred = model.U2NETP(3, 1)
    model_pred.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model_pred.to(device)  # Move model to appropriate device
    model_pred.eval()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    raise RuntimeError(f"Failed to load model: {e}")


def norm_pred(d: torch.Tensor) -> torch.Tensor:
    ma = torch.max(d)
    mi = torch.min(d)
    denom = ma - mi
    # Guard against divide-by-zero for flat tensors
    if denom.abs().item() < 1e-6:
        return torch.zeros_like(d)
    return (d - mi) / denom


def preprocess(image: Image.Image) -> torch.Tensor:
    # Ensure RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize to 320x320 like RescaleT(320)
    resized = image.resize((320, 320), resample=Image.BILINEAR)

    img_np = np.array(resized).astype(np.float32)

    # Match ToTensorLab(flag=0) behavior: normalize by max(img) if non-zero
    max_val = float(img_np.max())
    if max_val >= 1e-6:
        img_np = img_np / max_val

    tmp_img = np.zeros_like(img_np, dtype=np.float32)
    # Per-channel normalization
    tmp_img[:, :, 0] = (img_np[:, :, 0] - 0.485) / 0.229
    tmp_img[:, :, 1] = (img_np[:, :, 1] - 0.456) / 0.224
    tmp_img[:, :, 2] = (img_np[:, :, 2] - 0.406) / 0.225

    # HWC -> CHW
    tmp_img = np.transpose(tmp_img, (2, 0, 1))

    return torch.from_numpy(tmp_img)


def remove_bg(image: Image.Image, resize: bool = False) -> Image.Image:
    if image.mode != "RGB":
        image = image.convert("RGB")

    tensor_input = preprocess(image)

    with torch.inference_mode():
        inputs_test = tensor_input.unsqueeze(0).float().to(device)  # Move input to device

        outputs = model_pred(inputs_test)
        d1 = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
        pred = d1[:, 0, :, :]
        predict = norm_pred(pred).cpu().detach().numpy()  # Move to CPU before converting to numpy

        # Ensure the array is in the correct format for PIL
        if predict.ndim != 2:
            if predict.ndim == 3 and predict.shape[0] == 1:
                predict = predict[0]  # Remove the first dimension
            elif predict.ndim == 3 and predict.shape[2] == 1:
                predict = predict[:, :, 0]  # Remove the last dimension
        
        # Ensure the data is in the correct range and type
        predict = np.clip(predict, 0, 1)  # Clip to [0, 1] range
        predict = predict.astype(np.float32)  # Ensure float32 type
        
        # Convert to uint8 for PIL
        matte_array = (predict * 255).astype(np.uint8)
        
        matte = Image.fromarray(matte_array, mode='L')
        matte = matte.resize(image.size, resample=Image.BILINEAR)

        empty_img = Image.new("RGBA", image.size, 0)
        composed = Image.composite(image, empty_img, matte)

        return composed