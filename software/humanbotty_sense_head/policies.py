"""Local look-at policies. No motor publish. Supervisor owns commands."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass


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
    # Empty or inverted boxes are detector failures, not faces  -  a zero-area
    # box still yields a "center" that yanks the head toward noise.
    if w <= 0 or h <= 0:
        return pan, tilt
    # Boxes wholly outside the normalized frame still have positive w/h but
    # their "center" yanks the head toward detector garbage off-image.
    if x >= 1.0 or y >= 1.0 or (x + w) <= 0.0 or (y + h) <= 0.0:
        return pan, tilt
    cx = x + w * 0.5
    cy = y + h * 0.5
    # Partial clips can still place the geometric center outside the unit
    # square (e.g. x=-0.05,w=0.08 → cx=-0.01). Distinct from wholly-OOB.
    if not (0.0 <= cx <= 1.0 and 0.0 <= cy <= 1.0):
        return pan, tilt
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


@dataclass
class LookMemory:
    """Shared pose + last face/sound samples for the look arbiter."""

    pan: float = 0.0
    tilt: float = 0.0
    face_box: tuple[float, float, float, float] | None = None
    face_t: float = 0.0
    sound_yaw: float | None = None
    sound_t: float = 0.0


FACE_TTL_SEC = 0.35
SOUND_TTL_SEC = 0.50


def remember_pose(mem: LookMemory, pan: float, tilt: float) -> None:
    """Update current joints; ignore non-finite samples so NaN cannot stick."""
    if math.isfinite(pan) and math.isfinite(tilt):
        mem.pan = pan
        mem.tilt = tilt


def remember_face(
    mem: LookMemory,
    box: tuple[float, ...] | list[float],
    now: float,
) -> None:
    """Store a face box sample. Short/garbage payloads are ignored."""
    if box is None or len(box) < 4:
        return
    try:
        sample = (float(box[0]), float(box[1]), float(box[2]), float(box[3]))
    except (TypeError, ValueError):
        return
    if not all(math.isfinite(v) for v in sample):
        return
    mem.face_box = sample
    mem.face_t = now


def remember_sound(mem: LookMemory, yaw: float, now: float) -> None:
    """Store a sound yaw sample; non-finite yaw is dropped."""
    if yaw is None or not math.isfinite(yaw):
        return
    mem.sound_yaw = float(yaw)
    mem.sound_t = now


def tick_look(
    mem: LookMemory,
    now: float,
    rng: random.Random | None = None,
    face_gain: float = 0.6,
    sound_gain: float = 0.45,
    face_ttl: float = FACE_TTL_SEC,
    sound_ttl: float = SOUND_TTL_SEC,
) -> tuple[float, float]:
    """Blend fresh face/sound with idle saccade; advance mem pose."""
    face: tuple[float, float] | None = None
    if mem.face_box is not None and (now - mem.face_t) <= face_ttl:
        face = look_at_face(mem.face_box, mem.pan, mem.tilt, gain=face_gain)

    sound: tuple[float, float] | None = None
    if mem.sound_yaw is not None and (now - mem.sound_t) <= sound_ttl:
        sound = look_at_sound(mem.sound_yaw, mem.pan, mem.tilt, gain=sound_gain)

    idle = idle_saccade(mem.pan, mem.tilt, rng=rng)
    pan, tilt = blend(face, sound, idle)
    mem.pan, mem.tilt = pan, tilt
    return pan, tilt
