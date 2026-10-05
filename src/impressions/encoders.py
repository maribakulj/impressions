"""Three image encoders, all read from the local Hugging Face cache.

CLIP and SigLIP learned from captions, so phrases such as "a photo of a painting" are part of
what they know; DINOv2 learned from images alone. The comparison between the two families is the
control for the training-data question in PLAN.md.
"""

from __future__ import annotations

import os
from collections.abc import Iterable

import numpy as np
import torch
from PIL import Image

os.environ.setdefault("HF_HUB_OFFLINE", "1")

MODELS = {
    "clip": "openai/clip-vit-base-patch32",
    "siglip": "google/siglip-base-patch16-224",
    "dinov2": "facebook/dinov2-base",
}


def device() -> str:
    return "mps" if torch.backends.mps.is_available() else "cpu"


class Encoder:
    """Image (and, for CLIP/SigLIP, text) embeddings, L2-normalised, float32."""

    def __init__(self, name: str):
        from transformers import AutoImageProcessor, AutoModel, AutoProcessor

        self.name = name
        repo = MODELS[name]
        self.dev = device()
        self.model = AutoModel.from_pretrained(repo).to(self.dev).eval()
        if name == "dinov2":
            self.processor = AutoImageProcessor.from_pretrained(repo)
        else:
            self.processor = AutoProcessor.from_pretrained(repo)

    @torch.no_grad()
    def images(self, images: Iterable[Image.Image], batch: int = 32) -> np.ndarray:
        out, chunk = [], []
        for im in images:
            chunk.append(im.convert("RGB"))
            if len(chunk) == batch:
                out.append(self._images(chunk))
                chunk = []
        if chunk:
            out.append(self._images(chunk))
        return np.concatenate(out) if out else np.zeros((0, 0), np.float32)

    def _images(self, chunk: list[Image.Image]) -> np.ndarray:
        if self.name == "dinov2":
            inputs = self.processor(images=chunk, return_tensors="pt").to(self.dev)
            hidden = self.model(**inputs).last_hidden_state
            # CLS token and mean of patch tokens, as in the DINOv2 linear-probe recipe
            feats = torch.cat([hidden[:, 0], hidden[:, 1:].mean(1)], dim=1)
        else:
            inputs = self.processor(images=chunk, return_tensors="pt").to(self.dev)
            feats = self.model.get_image_features(**inputs)
            if not torch.is_tensor(feats):
                feats = feats.pooler_output
        feats = torch.nn.functional.normalize(feats.float(), dim=-1)
        return feats.cpu().numpy().astype(np.float32)

    @torch.no_grad()
    def texts(self, texts: list[str]) -> np.ndarray:
        if self.name == "dinov2":
            raise ValueError("DINOv2 has no text tower")
        kwargs = {"padding": "max_length", "max_length": 64} if self.name == "siglip" else {
            "padding": True}
        inputs = self.processor(text=texts, return_tensors="pt", truncation=True, **kwargs)
        inputs = inputs.to(self.dev)
        feats = self.model.get_text_features(**inputs)
        if not torch.is_tensor(feats):
            feats = feats.pooler_output
        feats = torch.nn.functional.normalize(feats.float(), dim=-1)
        return feats.cpu().numpy().astype(np.float32)
