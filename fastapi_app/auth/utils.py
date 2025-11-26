from fastapi import Request
from user_agents import parse


def collect_client_device_info(request: Request):
    ua_string = request.headers.get("User-Agent", "")
    ua = parse(ua_string)

    device = ua.device.family or "Unknown"
    os = ua.os.family or "Unknown"
    browser = ua.browser.family or "Unknown"

    return f"{device}|{os}|{browser}"
