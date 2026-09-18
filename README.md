# HumanBotty

**A public maker guide for building a physical body for an AI you already talk to.**

[![Live](https://img.shields.io/badge/live-humanbotty.jonbailey.xyz-111111)](https://humanbotty.jonbailey.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-informational)](VERSION)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%2F%20Jazzy-22314E)](software/)

Sense-first hybrid: a humanoid head and arms on a practical wheeled base. Phase 1 is a **Sense Head** (vision, audio, IMU, pan-tilt, hardware e-stop). Full biped is optional and late.

**Live guide:** [humanbotty.jonbailey.xyz](https://humanbotty.jonbailey.xyz/)

Not an xAI product. Not [AetherOS](https://aetheros.jonbailey.xyz/). Not [AXIOM](https://axiom.jonbailey.xyz/).

## Phase 1: Sense Head

| Piece | Role |
|-------|------|
| Vision + audio + IMU | See, hear, know orientation |
| Pan-tilt | Look at a face or a sound |
| Hardware e-stop | Cuts the servo rail. Software cannot skip it |
| `safety_supervisor` | Only publisher of `/humanbotty/head/joint_command` |

Motor commands never bypass the supervisor. The ROS package is the software half of that contract.

## Software (MIT)

ROS 2 package: [`software/`](software/). Guide: [software.html](https://humanbotty.jonbailey.xyz/software.html)

```
cd software
python -m unittest discover -s test -v
```

Humble or Jazzy. Pick one and stick.

```
cd /path/to/HumanBotty
ln -s "$(pwd)/software" ~/ros2_ws/src/humanbotty_sense_head
cd ~/ros2_ws
colcon build --packages-select humanbotty_sense_head
source install/setup.bash
ros2 launch humanbotty_sense_head sense_head.launch.py
```

## Site

Static files live in `public/`. Advertised version is `1.1.0` (`VERSION`). After copy edits:

```powershell
py -3 scripts/emit_pages.py
py -3 scripts/check_version.py
```

Ship the public folder with `.\deploy.ps1`.

## Related

| Tool | Role |
|------|------|
| [GrokLink OS](https://github.com/Pitchfork-and-Torch/GrokLink-OS) ([site](https://groklink.jonbailey.xyz/)) | Gated agent on portable radio hardware |
| [grok-orbit](https://github.com/Pitchfork-and-Torch/grok-orbit) | Desktop command center for the Grok fleet |
| [AetherOS](https://aetheros.jonbailey.xyz/) | Capability microkernel (not this body) |

## License

MIT. Pitchfork-and-Torch.
