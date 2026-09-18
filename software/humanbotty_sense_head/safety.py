"""Pure safety gate. Importable without ROS."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Limits:
    pan_min: float = -1.2
    pan_max: float = 1.2
    tilt_min: float = -0.6
    tilt_max: float = 0.7
    vel_max: float = 0.8
    watchdog_sec: float = 0.4
    # Software clear of a latched e-stop is opt-in (see safety.yaml).
    allow_clear_estop: bool = False


@dataclass
class SupervisorState:
    estop_latched: bool = False
    last_ok_monotonic: float = 0.0
    last_pan: float = 0.0
    last_tilt: float = 0.0


def clamp(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value


def latch_estop(state: SupervisorState, pressed: bool) -> SupervisorState:
    if pressed:
        state.estop_latched = True
    return state


def clear_estop(state: SupervisorState, allow_clear: bool) -> SupervisorState:
    if allow_clear:
        state.estop_latched = False
    return state


def watchdog_ok(state: SupervisorState, now: float, limits: Limits) -> bool:
    return (now - state.last_ok_monotonic) <= limits.watchdog_sec


def command_allowed(
    state: SupervisorState,
    now: float,
    limits: Limits,
    heartbeat_ok: bool,
) -> bool:
    if state.estop_latched:
        return False
    if not heartbeat_ok:
        return False
    if not watchdog_ok(state, now, limits):
        return False
    return True


def clamp_pose(pan: float, tilt: float, limits: Limits) -> tuple[float, float]:
    return (
        clamp(pan, limits.pan_min, limits.pan_max),
        clamp(tilt, limits.tilt_min, limits.tilt_max),
    )


def rate_limit(
    pan: float,
    tilt: float,
    state: SupervisorState,
    dt: float,
    limits: Limits,
) -> tuple[float, float]:
    if dt <= 0:
        return state.last_pan, state.last_tilt
    max_step = limits.vel_max * dt
    dpan = clamp(pan - state.last_pan, -max_step, max_step)
    dtilt = clamp(tilt - state.last_tilt, -max_step, max_step)
    return state.last_pan + dpan, state.last_tilt + dtilt


def gated_command(
    desired_pan: float,
    desired_tilt: float,
    state: SupervisorState,
    now: float,
    dt: float,
    limits: Limits,
    heartbeat_ok: bool,
) -> tuple[float, float, bool]:
    """Return (pan, tilt, allowed). Zeroes pose when blocked."""
    if not command_allowed(state, now, limits, heartbeat_ok):
        return state.last_pan, state.last_tilt, False
    pan, tilt = clamp_pose(desired_pan, desired_tilt, limits)
    pan, tilt = rate_limit(pan, tilt, state, dt, limits)
    state.last_pan = pan
    state.last_tilt = tilt
    state.last_ok_monotonic = now
    return pan, tilt, True
