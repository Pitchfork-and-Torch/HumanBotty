from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    safety_params = PathJoinSubstitution(
        [FindPackageShare("humanbotty_sense_head"), "config", "safety.yaml"]
    )
    return LaunchDescription(
        [
            Node(
                package="humanbotty_sense_head",
                executable="safety_supervisor",
                name="safety_supervisor",
                output="screen",
                parameters=[safety_params],
            ),
            Node(
                package="humanbotty_sense_head",
                executable="look_arbiter",
                name="look_arbiter",
                output="screen",
            ),
            Node(
                package="humanbotty_sense_head",
                executable="humanbotty_bridge",
                name="humanbotty_bridge",
                output="screen",
            ),
            Node(
                package="humanbotty_sense_head",
                executable="status_node",
                name="status_node",
                output="screen",
            ),
        ]
    )
