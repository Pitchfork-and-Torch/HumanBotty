"""Local look-at policies. No motor publish. Supervisor owns commands."""

from __future__ import annotations

import math
import random


def look_at_face(
    box_xywh: tuple[float, float, float, float] | None,
    pan: float,
    tilt: float,
    gain: float = 0.6,
) -> tuple[float, float]:
    """box is normalized [x, y, w, h] in image coords, origin top-left."""
    if not box_xywh:
        return pan, tilt
    x, y, w, h = box_xywh
    # Non-finite boxes (detector glitch) must not poison pan/tilt with NaN.
    if not all(math.isfinite(v) for v in (x, y, w, h)):
        return pan, tilt
    cx = x + w * 0.5
    cy = y + h * 0.5
    err_x = cx - 0.5
    err_y = 0.5 - cy
    return pan + (-err_x * gain), tilt + (err_y * gain)


def look_at_sound(
    yaw_rad: float | None,
    pan: float,
    tilt: float,
    gain: float = 0.45,
) -> tuple[float, float]:
    if yaw_rad is None or not math.isfinite(yaw_rad):
        return pan, tilt
    return pan + yaw_rad * gain, tilt


def idle_saccade(
    pan: float,
    tilt: float,
    rng: random.Random | None = None,
    max_step: float = 0.04,
) -> tuple[float, float]:
    r = rng or random
    return pan + r.uniform(-max_step, max_step), tilt + r.uniform(-max_step * 0.5, max_step * 0.5)


def blend(
    face: tuple[float, float] | None,
    sound: tuple[float, float] | None,
    idle: tuple[float, float],
    face_weight: float = 0.7,
    sound_weight: float = 0.3,
) -> tuple[float, float]:
    if face is not None:
        return face
    if sound is not None:
        return (
            idle[0] * (1.0 - sound_weight) + sound[0] * sound_weight,
            idle[1] * (1.0 - sound_weight) + sound[1] * sound_weight,
        )
    return idle
