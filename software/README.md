# HumanBotty Sense Head software

MIT ROS 2 package for Phase 1: a pan-tilt head that can see, hear, and look.

Motor commands never bypass `safety_supervisor`. Hardware e-stop still has to cut the servo rail. This package is the software half of that contract.

Site: https://humanbotty.jonbailey.xyz/software.html

## What you get

| Node | Role |
|------|------|
| `safety_supervisor` | Latches e-stop, watchdogs, clamps pan/tilt, is the only publisher of `/humanbotty/head/joint_command` |
| `look_arbiter` | One look publisher: blends face, sound, and idle into `/humanbotty/head/joint_desired` |
| `look_at_face` | Standalone face-box → desired pose (kept for tests / debug) |
| `look_at_sound` | Standalone sound-angle → desired pose (kept for tests / debug) |
| `humanbotty_bridge` | Optional LAN status to a desktop agent. Cannot command joints. |
| `status_node` | `/humanbotty/status` heartbeat |

Desired poses go to `/humanbotty/head/joint_desired`. Only the supervisor may emit `/humanbotty/head/joint_command`.

`/humanbotty/vision/face` is `std_msgs/Float32MultiArray` as `[x, y, w, h]` in normalized image coords (0-1). Do not add a face database. Boxes are ephemeral look targets only.

Software e-stop clear is fail-closed: `allow_clear: false` in `config/safety.yaml` unless you deliberately opt in.

Privacy mute is a hardware or OS mute, not a software flag in this package.

## Tests (no ROS)

From this folder:

```
python -m unittest discover -s test -v
```

## ROS 2 install

Humble or Jazzy. Pick one and stick.

```
cd /path/to/HumanBotty
ln -s "$(pwd)/software" ~/ros2_ws/src/humanbotty_sense_head
cd ~/ros2_ws
colcon build --packages-select humanbotty_sense_head
source install/setup.bash
ros2 launch humanbotty_sense_head sense_head.launch.py
```
