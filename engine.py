import numpy as np
from PIL import Image
import torch
import model
import os
import urllib.request

torch.set_num_threads(1)

# Model path
model_path = './u2netp.pth'

# Download model if it doesn't exist
def download_model():
    if not os.path.exists(model_path):
        print("Downloading U2-Net model...")
        url = "https://github.com/xuebinqin/U-2-Net/releases/download/v1.0/u2netp.pth"
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded successfully!")

# Download model on import
download_model()

# Load the model
model_pred = model.U2NETP(3, 1)
model_pred.load_state_dict(torch.load(model_path, map_location="cpu", weights_only=True))
model_pred.eval()


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
        inputs_test = tensor_input.unsqueeze(0).float()

        outputs = model_pred(inputs_test)
        d1 = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
        pred = d1[:, 0, :, :]
        predict = norm_pred(pred).squeeze().cpu().detach().numpy()

        matte = Image.fromarray((predict * 255).astype(np.uint8)).convert("L")
        matte = matte.resize(image.size, resample=Image.BILINEAR)

        empty_img = Image.new("RGBA", image.size, 0)
        composed = Image.composite(image, empty_img, matte)

        return composed