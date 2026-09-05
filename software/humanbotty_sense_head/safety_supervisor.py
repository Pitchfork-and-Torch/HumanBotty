"""ROS 2 node: only publisher of /humanbotty/head/joint_command."""

from __future__ import annotations

import time

from humanbotty_sense_head.safety import Limits, SupervisorState, gated_command, latch_estop


def _limits_from_params(node) -> Limits:
    return Limits(
        pan_min=float(node.declare_parameter("pan_min", -1.2).value),
        pan_max=float(node.declare_parameter("pan_max", 1.2).value),
        tilt_min=float(node.declare_parameter("tilt_min", -0.6).value),
        tilt_max=float(node.declare_parameter("tilt_max", 0.7).value),
        vel_max=float(node.declare_parameter("vel_max", 0.8).value),
        watchdog_sec=float(node.declare_parameter("watchdog_sec", 0.4).value),
    )


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Bool, Float32MultiArray

    class SafetySupervisor(Node):
        def __init__(self) -> None:
            super().__init__("safety_supervisor")
            self.limits = _limits_from_params(self)
            self.state = SupervisorState(last_ok_monotonic=time.monotonic())
            self.desired = (0.0, 0.0)
            self.last_tick = time.monotonic()
            self.create_subscription(Bool, "/humanbotty/safety/estop", self._on_estop, 10)
            self.create_subscription(
                Float32MultiArray, "/humanbotty/head/joint_desired", self._on_desired, 10
            )
            self.pub = self.create_publisher(Float32MultiArray, "/humanbotty/head/joint_command", 10)
            self.armed_pub = self.create_publisher(Bool, "/humanbotty/safety/armed", 10)
            self.create_timer(0.02, self._tick)

        def _on_estop(self, msg: Bool) -> None:
            latch_estop(self.state, bool(msg.data))
            if msg.data:
                self.get_logger().warn("e-stop latched")

        def _on_desired(self, msg: Float32MultiArray) -> None:
            if len(msg.data) >= 2:
                self.desired = (float(msg.data[0]), float(msg.data[1]))

        def _tick(self) -> None:
            now = time.monotonic()
            dt = now - self.last_tick
            self.last_tick = now
            pan, tilt, allowed = gated_command(
                self.desired[0],
                self.desired[1],
                self.state,
                now,
                dt,
                self.limits,
                heartbeat_ok=True,
            )
            out = Float32MultiArray()
            out.data = [pan, tilt]
            self.pub.publish(out)
            armed = Bool()
            armed.data = allowed
            self.armed_pub.publish(armed)

    rclpy.init(args=args)
    node = SafetySupervisor()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
