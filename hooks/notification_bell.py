"""
notification_bell.py
--------------------
Plays a sound or sends a desktop notification when Claude finishes a task.
Useful when running long tasks — you can walk away and get notified.

Hook type: Notification
Trigger:   * (all notifications)

Register in settings.json:
  "hooks": {
    "Notification": [
      {
        "matcher": "*",
        "hooks": [{"type": "command", "command": "python /path/to/notification_bell.py"}]
      }
    ]
  }
"""

import json
import sys
import os
import platform
import subprocess

# ── Config ────────────────────────────────────────────────────────────────────

# Set to True to use desktop notifications (requires platform support, see below)
USE_DESKTOP_NOTIFICATION = True

# Set to True to also print a terminal bell character
USE_TERMINAL_BELL = True

# ── Desktop notification helpers ──────────────────────────────────────────────

def notify_macos(title, message):
    """macOS: uses osascript (built-in, no install needed)"""
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def notify_linux(title, message):
    """Linux: uses notify-send (install: sudo apt install libnotify-bin)"""
    subprocess.run(["notify-send", title, message], capture_output=True)


def notify_windows(title, message):
    """
    Windows: uses PowerShell toast notification.
    No extra install needed on Windows 10+.
    """
    ps_script = f"""
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
        [Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $template.GetElementsByTagName('text')[0].AppendChild($template.CreateTextNode('{title}')) | Out-Null
    $template.GetElementsByTagName('text')[1].AppendChild($template.CreateTextNode('{message}')) | Out-Null
    $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show($toast)
    """
    subprocess.run(["powershell", "-Command", ps_script], capture_output=True)


def send_desktop_notification(title, message):
    system = platform.system()
    try:
        if system == "Darwin":
            notify_macos(title, message)
        elif system == "Linux":
            notify_linux(title, message)
        elif system == "Windows":
            notify_windows(title, message)
    except Exception:
        # Never crash Claude Code because of a notification failure
        pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    message = payload.get("message", "Task complete")
    title   = "Claude Code"

    if USE_TERMINAL_BELL:
        # ASCII bell character — rings the terminal
        print("\a", end="", flush=True)

    if USE_DESKTOP_NOTIFICATION:
        send_desktop_notification(title, message)

    # Notification hooks cannot block
    print(json.dumps({}))


if __name__ == "__main__":
    main()
