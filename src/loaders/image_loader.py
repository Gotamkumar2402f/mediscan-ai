"""Image helpers."""
from pathlib import Path
import hashlib
from PIL import Image

def save_uploaded_image(uploaded_file, out_dir: Path) -> str:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data = uploaded_file.getbuffer()
    h = hashlib.md5(data).hexdigest()[:8]
    name = f"{h}_{uploaded_file.name}"
    path = out_dir / name
    with open(path, "wb") as f:
        f.write(data)
    return str(path)

def is_valid_image(path: str) -> bool:
    try:
        Image.open(path).verify()
        return True
    except Exception:
        return False