import os

from blue_objects import file, README

from blue_rover import NAME, VERSION, ICON, REPO_NAME


items = README.Items(
    [
        {
            "name": "blue-rover",
            "marquee": "https://github.com/waveshareteam/ugv_rpi/raw/main/media/UGV-Rover-details-23.jpg",
            "description": "starting off on a [UGV Beast PI ROS2](https://www.waveshare.com/wiki/UGV_Beast_PI_ROS2#ROS2_open_source_project)...",
        },
    ]
)


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
