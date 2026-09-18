"""Heartbeat on /humanbotty/status."""

from __future__ import annotations

import json
import time


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class Status(Node):
        def __init__(self) -> None:
            super().__init__("status_node")
            self.pub = self.create_publisher(String, "/humanbotty/status", 10)
            self.t0 = time.monotonic()
            self.create_timer(0.5, self._tick)

        def _tick(self) -> None:
            msg = String()
            msg.data = json.dumps(
                {
                    "uptime_s": round(time.monotonic() - self.t0, 1),
                    "package": "humanbotty_sense_head",
                }
            )
            self.pub.publish(msg)

    rclpy.init(args=args)
    node = Status()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
