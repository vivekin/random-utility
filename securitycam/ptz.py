"""
Simple PTZ camera control via ONVIF.

Requires:
    pip install onvif-zeep

Notes:
- RTSP (554) is only used for viewing the video stream, not for control.
- PTZ commands go through the ONVIF SOAP service (port 2020 here).
- Update IP, port, username, and password below to match your camera.
"""

from onvif import ONVIFCamera
import time


# ---- Camera connection settings ----
CAMERA_IP = "192.168.1.10"   # ONVIF host (from your onvif/device_service URL)
CAMERA_PORT = 2020              # ONVIF port
USERNAME = ""               # change to your camera's username
PASSWORD = ""       # change to your camera's password


def connect_camera():
    cam = ONVIFCamera(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD)
    media = cam.create_media_service()
    ptz = cam.create_ptz_service()
    profile = media.GetProfiles()[0]  # use the first media profile
    return ptz, profile


def move(ptz, profile, pan=0.0, tilt=0.0, zoom=0.0, duration=1.0):
    """
    pan/tilt/zoom range: -1.0 to 1.0
    duration: seconds to move before stopping
    """
    request = ptz.create_type("ContinuousMove")
    request.ProfileToken = profile.token
    request.Velocity = {
        "PanTilt": {"x": pan, "y": tilt},
        "Zoom": {"x": zoom},
    }
    ptz.ContinuousMove(request)
    time.sleep(duration)
    stop(ptz, profile)


def stop(ptz, profile):
    request = ptz.create_type("Stop")
    request.ProfileToken = profile.token
    request.PanTilt = True
    request.Zoom = True
    ptz.Stop(request)


def get_position(ptz, profile):
    """
    Query the camera's current PTZ position.
    Returns the raw Status object - not all cameras report Position
    (some only report MoveStatus), so check both.
    """
    status = ptz.GetStatus({"ProfileToken": profile.token})

    if status.Position is not None:
        if status.Position.PanTilt is not None:
            pan = status.Position.PanTilt.x
            tilt = status.Position.PanTilt.y
            print(f"Pan: {pan:.3f}, Tilt: {tilt:.3f}")
        else:
            print("Camera does not report PanTilt position.")

        if status.Position.Zoom is not None:
            zoom = status.Position.Zoom.x
            print(f"Zoom: {zoom:.3f}")
        else:
            print("Camera does not report Zoom position.")
    else:
        print("Camera does not report absolute Position.")

    if status.MoveStatus is not None:
        print(f"MoveStatus: {status.MoveStatus}")

    return status


def set_current_position_as_home(ptz, profile):
    """
    Reads the camera's current PTZ position, prints it, then saves
    that exact position as the home position.
    Note: SetHomePosition doesn't take coordinates - it always saves
    wherever the camera currently is.
    """
    print("Reading current position...")
    status = get_position(ptz, profile)

    print("Saving current position as home...")
    request = ptz.create_type("SetHomePosition")
    request.ProfileToken = profile.token
    ptz.SetHomePosition(request)

    print("Home position set.")
    return status


def set_home(ptz, profile):
    """Save the camera's CURRENT position as the home position."""
    request = ptz.create_type("SetHomePosition")
    request.ProfileToken = profile.token
    ptz.SetHomePosition(request)


def goto_home(ptz, profile):
    """
    Move to the saved home position.
    Not all cameras support this - if none has been set, the camera
    will reject the request with a SOAP fault. We catch that here
    instead of crashing.
    """
    try:
        request = ptz.create_type("GotoHomePosition")
        request.ProfileToken = profile.token
        ptz.GotoHomePosition(request)
    except Exception as e:
        print(f"GotoHomePosition not supported or no home set: {e}")


if __name__ == "__main__":
    ptz, profile = connect_camera()

    print("Current position:")
    get_position(ptz, profile)

    print("Panning right...")
    move(ptz, profile, pan=0.5, tilt=0.0, duration=1.5)

    print("Panning left...")
    move(ptz, profile, pan=-0.5, tilt=0.0, duration=1.5)

    print("Tilting up...")
    move(ptz, profile, pan=0.0, tilt=0.5, duration=1.5)

    print("Tilting down...")
    move(ptz, profile, pan=0.0, tilt=-0.5, duration=1.5)

    print("Zooming in...")
    move(ptz, profile, zoom=0.5, duration=1.5)

    print("Returning to home position...")
    goto_home(ptz, profile)

    print("Done.")
