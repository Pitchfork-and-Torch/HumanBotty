"""Optional LAN status to a desktop agent. Cannot publish joint commands."""

from __future__ import annotations

import json
import socket


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Bool, Float32MultiArray

    class Bridge(Node):
        def __init__(self) -> None:
            super().__init__("humanbotty_bridge")
            self.host = str(self.declare_parameter("agent_host", "127.0.0.1").value)
            self.port = int(self.declare_parameter("agent_port", 0).value)
            self.armed = False
            self.pose = (0.0, 0.0)
            self.create_subscription(Bool, "/humanbotty/safety/armed", self._on_armed, 10)
            self.create_subscription(
                Float32MultiArray, "/humanbotty/head/joint_states", self._on_state, 10
            )
            self.create_timer(1.0, self._emit)

        def _on_armed(self, msg: Bool) -> None:
            self.armed = bool(msg.data)

        def _on_state(self, msg: Float32MultiArray) -> None:
            if len(msg.data) >= 2:
                self.pose = (float(msg.data[0]), float(msg.data[1]))

        def _emit(self) -> None:
            payload = json.dumps(
                {
                    "armed": self.armed,
                    "pan": self.pose[0],
                    "tilt": self.pose[1],
                    "note": "status only; joints are owned by safety_supervisor",
                }
            ).encode("utf-8")
            if self.port <= 0:
                self.get_logger().debug(payload.decode("utf-8"))
                return
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.sendto(payload, (self.host, self.port))
            finally:
                sock.close()

    rclpy.init(args=args)
    node = Bridge()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
