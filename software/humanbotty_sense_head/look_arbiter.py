"""Publish one desired look pose from face, sound, and idle.

Never commands joints. Never stores images or identities.
"""

from __future__ import annotations

import random
import time

from humanbotty_sense_head.policies import (
    LookMemory,
    remember_face,
    remember_pose,
    remember_sound,
    tick_look,
)


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32, Float32MultiArray

    class LookArbiter(Node):
        def __init__(self) -> None:
            super().__init__("look_arbiter")
            self.mem = LookMemory()
            self.rng = random.Random()
            self.face_gain = float(self.declare_parameter("gain", 0.6).value)
            self.sound_gain = float(self.declare_parameter("sound_gain", 0.45).value)
            self.create_subscription(
                Float32MultiArray, "/humanbotty/vision/face", self._on_face, 10
            )
            self.create_subscription(Float32, "/humanbotty/audio/angle", self._on_angle, 10)
            self.create_subscription(
                Float32MultiArray, "/humanbotty/head/joint_states", self._on_state, 10
            )
            self.pub = self.create_publisher(
                Float32MultiArray, "/humanbotty/head/joint_desired", 10
            )
            self.create_timer(0.05, self._tick)

        def _on_state(self, msg: Float32MultiArray) -> None:
            if len(msg.data) < 2:
                return
            try:
                remember_pose(self.mem, float(msg.data[0]), float(msg.data[1]))
            except (TypeError, ValueError):
                return

        def _on_face(self, msg: Float32MultiArray) -> None:
            try:
                box = tuple(float(v) for v in msg.data)
            except (TypeError, ValueError):
                return
            remember_face(self.mem, box, time.monotonic())

        def _on_angle(self, msg: Float32) -> None:
            try:
                yaw = float(msg.data)
            except (TypeError, ValueError):
                return
            remember_sound(self.mem, yaw, time.monotonic())

        def _tick(self) -> None:
            pan, tilt = tick_look(
                self.mem,
                time.monotonic(),
                rng=self.rng,
                face_gain=self.face_gain,
                sound_gain=self.sound_gain,
            )
            out = Float32MultiArray()
            out.data = [pan, tilt]
            self.pub.publish(out)

    rclpy.init(args=args)
    node = LookArbiter()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
