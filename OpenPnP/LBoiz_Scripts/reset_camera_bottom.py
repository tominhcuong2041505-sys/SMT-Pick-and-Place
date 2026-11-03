import os

DEV = "/dev/video3"
CONTROLS = [
    "white_balance_automatic=1",
    "auto_exposure=3",
    "brightness=-64",
    "contrast=40",
    "saturation=66",
    "hue=0",
    "gamma=100",
    "sharpness=2",
    "power_line_frequency=1",
    "white_balance_temperature=4600",
    "backlight_compensation=0",
    "focus_automatic_continuous=1",
]

for ctrl in CONTROLS:
    os.system("v4l2-ctl -d " + DEV + " --set-ctrl=" + ctrl + " > /dev/null 2>&1")
