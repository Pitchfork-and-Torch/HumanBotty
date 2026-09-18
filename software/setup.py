from setuptools import find_packages, setup

package_name = "humanbotty_sense_head"

setup(
    name=package_name,
    version="1.2.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/sense_head.launch.py"]),
        ("share/" + package_name + "/config", ["config/safety.yaml"]),
        ("share/" + package_name + "/urdf", ["urdf/sense_head.urdf"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Pitchfork-and-Torch",
    maintainer_email="297513015+Pitchfork-and-Torch@users.noreply.github.com",
    description="HumanBotty Phase 1 Sense Head ROS 2 nodes.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "safety_supervisor = humanbotty_sense_head.safety_supervisor:main",
            "look_at_face = humanbotty_sense_head.look_at_face:main",
            "look_at_sound = humanbotty_sense_head.look_at_sound:main",
            "humanbotty_bridge = humanbotty_sense_head.bridge:main",
            "status_node = humanbotty_sense_head.status_node:main",
            "look_arbiter = humanbotty_sense_head.look_arbiter:main",
        ],
    },
)
