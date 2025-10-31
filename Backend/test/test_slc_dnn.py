# tests/test_slc_dnn.py
import pytest
from fastapi.testclient import TestClient
import numpy as np

from src.app import app

# Adjust to your route module path
import src.routes.slc_dnn as slc_dnn_module

client = TestClient(app)


@pytest.fixture
def dummy_interpreter():
    """
    Create a simple dummy TFLite-like interpreter object with the minimal API
    used by the route (get_input_details, get_output_details, set_tensor, invoke, get_tensor).
    This allows tests to run without a real TFLite binary.
    """
    class DummyInterpreter:
        def __init__(self, output_probs):
            self._output = np.array([output_probs], dtype=np.float32)
            self._input_index = 0
            self._output_index = 0

        def allocate_tensors(self):
            return None

        def get_input_details(self):
            return [{"index": self._input_index, "shape": np.array([1, 42], dtype=np.int32)}]

        def get_output_details(self):
            return [{"index": self._output_index, "shape": np.array([1, len(self._output[0])], dtype=np.int32)}]

        def set_tensor(self, index, value):
            # simple check: shape should be (1, 42)
            assert value.shape[1] == 42

        def invoke(self):
            pass

        def get_tensor(self, index):
            return self._output

    return DummyInterpreter


def test_slc_dnn_predict_success(monkeypatch, dummy_interpreter):
    # Prepare dummy labels and interpreter that predicts class index 3 (e.g., 'D')
    fake_labels = np.array(["A", "B", "C", "D", "E"])
    # Soft probabilities: highest at index 3
    probs = [0.01, 0.01, 0.01, 0.96, 0.01]
    dummy = dummy_interpreter(probs)

    # Patch the interpreter and labels in the route module (import-time objects)
    monkeypatch.setattr(slc_dnn_module, "interpreter", dummy)
    monkeypatch.setattr(slc_dnn_module, "labels", fake_labels)

    # Build valid landmark payload (42 floats)
    landmarks = [float(i) * 0.001 for i in range(42)]
    resp = client.post("/slc-realtime/predict", json={"landmarks": landmarks})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["label"] == "D"
    assert pytest.approx(data["confidence"], rel=1e-3) == 0.96


def test_slc_dnn_predict_invalid_length(monkeypatch):
    # Ensure interpreter is present, but we won't reach invoke due to validation
    monkeypatch.setattr(slc_dnn_module, "interpreter", object())
    monkeypatch.setattr(slc_dnn_module, "labels", np.array(["A", "B", "C"]))

    # Send wrong number of landmarks
    landmarks = [0.0] * 10
    resp = client.post("/slc-realtime/predict", json={"landmarks": landmarks})
    assert resp.status_code == 400
    assert "Expected 42" in resp.json()["detail"]
