# HumanBotty Sense Head software

MIT ROS 2 package for Phase 1: a pan-tilt head that can see, hear, and look.

Motor commands never bypass `safety_supervisor`. Hardware e-stop still has to cut the servo rail. This package is the software half of that contract.

Site: https://humanbotty.jonbailey.xyz/software.html

## What you get

| Node | Role |
|------|------|
| `safety_supervisor` | Latches e-stop, watchdogs, clamps pan/tilt, is the only publisher of `/humanbotty/head/joint_command` |
| `look_at_face` | Turns a face box into a desired look pose |
| `look_at_sound` | Turns a sound angle into a desired look pose |
| `humanbotty_bridge` | Optional LAN status to a desktop agent. Cannot command joints. |
| `status_node` | `/humanbotty/status` heartbeat |

Desired poses go to `/humanbotty/head/joint_desired`. Only the supervisor may emit `/humanbotty/head/joint_command`.

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

On Windows, copy or junction `software` into your workspace `src` folder the same way.

## Topics

```
/humanbotty/camera/color/image_raw
/humanbotty/camera/depth/image_raw
/humanbotty/imu/data
/humanbotty/audio/vad
/humanbotty/vision/face
/humanbotty/audio/angle
/humanbotty/head/joint_states
/humanbotty/head/joint_desired
/humanbotty/head/joint_command
/humanbotty/safety/estop
/humanbotty/status
```

`/humanbotty/vision/face` is `std_msgs/Float32MultiArray` as `[x, y, w, h]` in normalized image coords (0-1). Swap in a real detector later.

`/humanbotty/safety/estop` is `std_msgs/Bool` (true = pressed). The supervisor latches until you publish false **and** restart is allowed in `config/safety.yaml`.

## Hard rules

- Do not publish `/humanbotty/head/joint_command` from any other node.
- Do not treat a software e-stop as a substitute for the mushroom switch on the servo rail.
- No weapons. No covert capture. Privacy mute is a hardware or OS mute, not a flag in this package.
