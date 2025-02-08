from setuptools import setup, find_packages

setup(
    name="capture_bot",
    version="0.1.0",
    description="A Python project for screen capture",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pyautogui",
        "pynput"
    ],
    entry_points={
        'console_scripts': [
            'run_capture_agent=screen_capture_agent.capture_agent:run_app',
        ],
    },
)
