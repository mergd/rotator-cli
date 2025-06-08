"""Inlined orientation detection model.

This module replaces the check-orientation dependency to avoid the FutureWarning
and reduce external dependencies.
"""

from typing import Optional

import torch.nn as nn
from timm import create_model as timm_create_model
from torch.utils import model_zoo


def create_orientation_model(activation: Optional[str] = "softmax") -> nn.Module:
    """Create the orientation detection model.

    This replaces check_orientation.pre_trained_models.create_model() to avoid
    the FutureWarning from old PyTorch model format.

    Args:
        activation: Whether to add softmax activation. Defaults to "softmax".

    Returns:
        The orientation detection model.
    """
    # Create the base model (ResNeXt50)
    model = timm_create_model("swsl_resnext50_32x4d", pretrained=False, num_classes=4)

    # Load the pre-trained weights
    url = "https://github.com/ternaus/check_orientation/releases/download/v0.0.3/2020-11-16_resnext50_32x4d.zip"
    state_dict = model_zoo.load_url(url, progress=True, map_location="cpu")[
        "state_dict"
    ]

    # Remove the "model." prefix from layer names
    cleaned_state_dict = {}
    for key, value in state_dict.items():
        if key.startswith("model."):
            cleaned_state_dict[key[6:]] = value  # Remove "model." prefix
        else:
            cleaned_state_dict[key] = value

    model.load_state_dict(cleaned_state_dict)

    if activation == "softmax":
        return nn.Sequential(model, nn.Softmax(dim=1))

    return model
