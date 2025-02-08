# capture_agent.py

import os
import time
import json
from datetime import datetime
from pathlib import Path

import pyautogui
from pynput import mouse, keyboard

class BackendInterface:
    """
    Base interface for any backend used by the CaptureAgent.
    You can implement cloud integration (e.g., AWS) by extending this class.
    """
    def store_screenshot(self, timestamp: str, screenshot_path: str):
        """
        Called when a new screenshot is captured.
        :param timestamp: ISO timestamp string.
        :param screenshot_path: Path to the saved screenshot.
        """
        raise NotImplementedError

    def store_action_event(self, action_event: dict):
        """
        Called when a new user action (mouse click, keyboard press, etc.) is recorded.
        :param action_event: A dictionary describing the event.
        """
        raise NotImplementedError

    def get_predicted_action(self, current_screenshot_path: str):
        """
        (Optional/Stub) If you have a model or a cloud service that returns
        predicted actions for the current screenshot, implement it here.
        :param current_screenshot_path: Path to the current screenshot file.
        :return: A dictionary describing the action, or None if no action.
        """
        raise NotImplementedError

    def store_executed_action(self, executed_action: dict):
        """
        Called after the agent executes an action (e.g., AI-based click).
        :param executed_action: A dictionary describing the action that was taken.
        """
        raise NotImplementedError


class LocalDiskBackend(BackendInterface):
    """
    A local filesystem implementation of BackendInterface.
    - Saves screenshots to: <output_dir>/screenshots/
    - Appends all events to: <output_dir>/actions.jsonl
    """
    def __init__(self, output_dir="output_data"):
        self.output_dir = Path(output_dir)
        self.screenshots_dir = self.output_dir / "screenshots"
        self.actions_file = self.output_dir / "actions.jsonl"

        # Create necessary directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.actions_file.touch(exist_ok=True)

    def store_screenshot(self, timestamp: str, screenshot_path: str):
        event = {
            "timestamp": timestamp,
            "type": "screenshot",
            "path": screenshot_path
        }
        self._append_event(event)

    def store_action_event(self, action_event: dict):
        self._append_event(action_event)

    def get_predicted_action(self, current_screenshot_path: str):
        # Stub: replace with your cloud or AI logic.
        return None

    def store_executed_action(self, executed_action: dict):
        self._append_event(executed_action)

    def _append_event(self, event: dict):
        with open(self.actions_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")


class CaptureAgent:
    """
    Orchestrates:
    - Screenshot capture at a fixed framerate
    - Mouse/keyboard listeners
    - Storing events via a backend
    - Optionally executing predicted actions
    """
    def __init__(self, backend: BackendInterface, framerate: float = 1.0):
        """
        :param backend: An implementation of BackendInterface (e.g., LocalDiskBackend).
        :param framerate: Screenshots per second (float). 1.0 = 1 screenshot/sec.
        """
        self.backend = backend
        self.framerate = framerate
        self._stop_flag = False

        # Mouse/keyboard listeners
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll,
            on_move=self.on_mouse_move
        )
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )

    def start_listeners(self):
        """Start mouse and keyboard event listeners in background threads."""
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listeners(self):
        """Stop mouse and keyboard listeners."""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def on_mouse_click(self, x, y, button, pressed):
        """Triggered when the mouse is clicked."""
        if pressed:
            event = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": str(button)
            }
            self.backend.store_action_event(event)

    def on_mouse_scroll(self, x, y, dx, dy):
        """Triggered when the mouse scrolls."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "mouse_scroll",
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy
        }
        self.backend.store_action_event(event)

    def on_mouse_move(self, x, y):
        """Optional: record mouse movement; commented out to reduce log spam."""
        # event = {
        #     "timestamp": datetime.utcnow().isoformat(),
        #     "type": "mouse_move",
        #     "x": x,
        #     "y": y
        # }
        # self.backend.store_action_event(event)
        pass

    def on_key_press(self, key):
        """Triggered when a key is pressed."""
        try:
            key_str = key.char  # For alphanumeric
        except AttributeError:
            key_str = str(key)  # For special keys (enter, space, etc.)

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "keyboard_press",
            "key": key_str
        }
        self.backend.store_action_event(event)

    def on_key_release(self, key):
        """Optional: record key release event."""
        # try:
        #     key_str = key.char
        # except AttributeError:
        #     key_str = str(key)
        # event = {
        #     "timestamp": datetime.utcnow().isoformat(),
        #     "type": "keyboard_release",
        #     "key": key_str
        # }
        # self.backend.store_action_event(event)
        pass

    def run_capture_loop(self):
        """
        Main capture loop:
          - Takes screenshots
          - Stores them in the backend
          - (Optional) Queries the backend for predicted actions
          - Executes predicted actions if any
        """
        print("[CaptureAgent] Starting capture loop. Press Ctrl+C to stop...")
        self.start_listeners()
        try:
            while not self._stop_flag:
                timestamp = datetime.utcnow().isoformat()
                screenshot_path = self._capture_screenshot(timestamp)
                self.backend.store_screenshot(timestamp, screenshot_path)

                # Check if there's a predicted action
                predicted_action = self.backend.get_predicted_action(screenshot_path)
                if predicted_action:
                    self.execute_action(predicted_action)
                    self.backend.store_executed_action(predicted_action)

                time.sleep(1.0 / self.framerate)
        except KeyboardInterrupt:
            print("\n[CaptureAgent] Stopping due to KeyboardInterrupt.")
        finally:
            self.stop()

    def _capture_screenshot(self, timestamp: str):
        """
        Takes a screenshot and saves it locally with a timestamp-based name.
        :return: The path to the saved screenshot.
        """
        output_path = self.backend.output_dir / "screenshots"  # type: ignore
        filename = f"screenshot_{timestamp.replace(':', '-')}.png"
        filepath = output_path / filename

        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        return str(filepath)

    def execute_action(self, action: dict):
        """
        Executes a predicted action, e.g.:
          {"type": "click", "x": 500, "y": 300, "button": "left"}
        or
          {"type": "keyboard_type", "text": "hello world"}
        """
        action_type = action.get("type")
        if action_type == "click":
            x = action.get("x")
            y = action.get("y")
            button = action.get("button", "left")
            print(f"[CaptureAgent] Executing click at ({x}, {y}) with button={button}")
            pyautogui.click(x=x, y=y, button=button)

        elif action_type == "keyboard_type":
            text = action.get("text", "")
            print(f"[CaptureAgent] Executing keyboard input: {text}")
            pyautogui.typewrite(text)

        else:
            print(f"[CaptureAgent] No recognized action type to execute: {action}")

    def stop(self):
        """Stops the capture loop and listeners."""
        self._stop_flag = True
        self.stop_listeners()
        print("[CaptureAgent] Capture agent stopped.")


def run_app():
    """
    Example entry point. Creates a LocalDiskBackend, instantiates CaptureAgent,
    and starts the capture loop.
    """
    os.environ['DISPLAY'] = ':0'  # Initialize DISPLAY environment variable
    backend = LocalDiskBackend(output_dir="output_data")
    agent = CaptureAgent(backend=backend, framerate=1.0)
    agent.run_capture_loop()
