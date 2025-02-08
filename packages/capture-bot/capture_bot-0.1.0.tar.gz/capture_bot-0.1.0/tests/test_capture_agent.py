from screen_capture_agent.capture_agent import CaptureAgent, LocalDiskBackend

def test_capture_agent_one_step():
    backend = LocalDiskBackend(output_dir="test_output")
    agent = CaptureAgent(backend=backend, framerate=1.0)
    
    # Start listeners (optional if you want to test input capture)
    agent.start_listeners()
    
    # Perform just ONE iteration of the capture logic (no infinite loop)
    timestamp = "2025-02-08T12:00:00"
    screenshot_path = agent._capture_screenshot(timestamp)
    backend.store_screenshot(timestamp, screenshot_path)
    
    predicted_action = backend.get_predicted_action(screenshot_path)
    if predicted_action:
        agent.execute_action(predicted_action)
        backend.store_executed_action(predicted_action)

    # Stop the listeners to finish the test
    agent.stop_listeners()
