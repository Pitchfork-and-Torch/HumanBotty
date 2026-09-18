"""Publish a desired look pose from a normalized face box. Never commands joints."""

from __future__ import annotations

from humanbotty_sense_head.policies import look_at_face


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32MultiArray

    class LookAtFace(Node):
        def __init__(self) -> None:
            super().__init__("look_at_face")
            self.pan = 0.0
            self.tilt = 0.0
            self.gain = float(self.declare_parameter("gain", 0.6).value)
            self.create_subscription(
                Float32MultiArray, "/humanbotty/vision/face", self._on_face, 10
            )
            self.create_subscription(
                Float32MultiArray, "/humanbotty/head/joint_states", self._on_state, 10
            )
            self.pub = self.create_publisher(
                Float32MultiArray, "/humanbotty/head/joint_desired", 10
            )

        def _on_state(self, msg: Float32MultiArray) -> None:
            if len(msg.data) >= 2:
                self.pan, self.tilt = float(msg.data[0]), float(msg.data[1])

        def _on_face(self, msg: Float32MultiArray) -> None:
            box = None
            if len(msg.data) >= 4:
                box = (float(msg.data[0]), float(msg.data[1]), float(msg.data[2]), float(msg.data[3]))
            pan, tilt = look_at_face(box, self.pan, self.tilt, gain=self.gain)
            out = Float32MultiArray()
            out.data = [pan, tilt]
            self.pub.publish(out)

    rclpy.init(args=args)
    node = LookAtFace()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
