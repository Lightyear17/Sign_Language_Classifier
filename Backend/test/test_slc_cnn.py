# tests/test_slc_cnn.py
import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import sys, os

# Ensure backend src is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app
import src.routes.slc_cnn as slc_module

client = TestClient(app)


@pytest.fixture(autouse=True)
def patch_predict_gesture(monkeypatch):
    """Monkeypatch predict_gesture to return fake output."""
    def fake_predict_gesture(img, interpreter, labels):
        return {"label": "A", "confidence": 0.912}
    monkeypatch.setattr(slc_module, "predict_gesture", fake_predict_gesture)
    yield


def make_valid_image_bytes() -> bytes:
    """Generate a small valid PNG image entirely in memory (so OpenCV can read it)."""
    buf = io.BytesIO()
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))  # red block
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


def test_slc_static_predict_file_success():
    img_bytes = make_valid_image_bytes()
    files = {"file": ("hand.png", io.BytesIO(img_bytes), "image/png")}

    resp = client.post("/slc-static/predict", files=files)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["label"] == "A"
    assert pytest.approx(data["confidence"], rel=1e-3) == 0.912


def test_slc_static_predict_invalid_file_type():
    """Should return 400 or 422 for non-image file."""
    files = {"file": ("not_image.txt", io.BytesIO(b"hello world"), "text/plain")}
    resp = client.post("/slc-static/predict", files=files)
    assert resp.status_code in (400, 422), resp.text
