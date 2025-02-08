# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

from qai_hub_models.models._shared.fastsam.model import Fast_SAM

MODEL_ID = __name__.split(".")[-2]
DEFAULT_WEIGHTS = "FastSAM-s.pt"
MODEL_ASSET_VERSION = 1


class FastSAM_S(Fast_SAM):
    """Exportable FastSAM model, end-to-end."""

    @classmethod
    def from_pretrained(cls, ckpt_name: str = DEFAULT_WEIGHTS):
        return Fast_SAM.from_pretrained.__func__(FastSAM_S, ckpt_name)
