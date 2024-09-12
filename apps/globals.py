import re

UNKNOWN = [
    "86-A4-83-79-44-65",
    "DE-ED-A5-24-46-5A",
    "0E-1A-B0-54-B5-94",
    "06-38-04-3F-06-32"
]
EVENTS = [
    "tplink_router_new_device",
    "tplink_router_device_offline",
    "tplink_router_device_online"
]
PATTERNS = {
    "motion": re.compile(r"binary_sensor\.(.*)_motion_occupancy"),
    "dimmer": re.compile(r"sensor\.(.*)_dimmer_action")
}

def enabled(state):
    return True if state == "on" else False

def get_motion_sensor(entity):
    match = re.fullmatch(PATTERNS["motion"], entity)
    if match:
        return f"light.{match.group(1)}", f"scene.{match.group(1)}_day", f"scene.{match.group(1)}_night"
    raise ValueError(f"Invalid motion sensor entity: {entity}")

def get_dimmer(entity):
    match = re.fullmatch(PATTERNS["dimmer"], entity)
    if match:
        return f"light.{match.group(1)}", f"scene.{match.group(1)}_day", f"scene.{match.group(1)}_night"
    raise ValueError(f"Invalid dimmer entity: {entity}")