from __future__ import annotations

from typing import Any, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


class FrameProcessor(Protocol):
    """Shared interface for computer vision modules."""

    def process_frame(
        self,
        frame: np.ndarray
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """
        Process one frame and return:
        - Annotated OpenCV frame
        - Dictionary containing module metrics
        """
        ...