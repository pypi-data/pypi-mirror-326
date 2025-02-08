# capture_bot
Get data from a computer

## Purpose and Main Functionalities

`capture_bot` is a tool designed to capture screenshots and record user actions such as mouse clicks and keyboard presses. It can be used for various purposes, including monitoring user activity, creating tutorials, and automating repetitive tasks.

## Installing Dependencies

To install the dependencies required to run `capture_bot`, use the following command:

```sh
pip install .
```

## Running the Capture Agent

To run the capture agent, use the provided `run_capture_agent` script. This script will start the capture agent, which will begin capturing screenshots and recording user actions.

```sh
run_capture_agent
```

## Examples

Here are some examples of how to start the capture agent and configure it:

1. Start the capture agent with the default settings:

```sh
run_capture_agent
```

2. Start the capture agent with a custom output directory:

```sh
run_capture_agent --output-dir custom_output
```

3. Start the capture agent with a custom framerate:

```sh
run_capture_agent --framerate 2.0
```
