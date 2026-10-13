import os
import sys
import time
import signal
import threading
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from key_listener import KeyListener
from result_thread import ResultThread
from transcription import create_local_model
from input_simulation import InputSimulator
from utils import ConfigManager


class HeadlessWhisperWriter:
    """
    Headless version of WhisperWriter for Task Scheduler
    Runs without GUI components - only hotkey listening and transcription
    """
    
    def __init__(self):
        print("Starting WhisperWriter in headless mode...")
        
        # Initialize configuration
        ConfigManager.initialize()
        
        if not ConfigManager.config_file_exists():
            print("ERROR: No configuration file found. Please run the GUI version first to set up configuration.")
            sys.exit(1)
            
        # Initialize threading components first
        self.result_thread = None
        self.running = True
        
        self.input_simulator = InputSimulator()
        self.key_listener = KeyListener()
        self.key_listener.add_callback("on_activate", self.on_activation)
        self.key_listener.add_callback("on_deactivation", self.on_deactivation)
        
        # Create local model if not using API
        model_options = ConfigManager.get_config_section('model_options')
        print("Creating local model...")
        self.local_model = create_local_model() if not model_options.get('use_api') else None
        print("Local model ready.")
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, sig, frame):
        """Handle shutdown signals gracefully"""
        print(f"Received signal {sig}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
        
    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'key_listener') and self.key_listener:
                self.key_listener.stop()
        except Exception as e:
            print(f"Error stopping key listener: {e}")
            
        try:
            if hasattr(self, 'input_simulator') and self.input_simulator:
                self.input_simulator.cleanup()
        except Exception as e:
            print(f"Error cleaning up input simulator: {e}")
            
        try:
            if hasattr(self, 'result_thread') and self.result_thread and hasattr(self.result_thread, 'isRunning') and self.result_thread.isRunning():
                self.result_thread.stop()
        except Exception as e:
            print(f"Error stopping result thread: {e}")
            
    def on_activation(self):
        """Called when the activation key combination is pressed."""
        print("Activation key pressed!")
        
        if self.result_thread and self.result_thread.isRunning():
            recording_mode = ConfigManager.get_config_value('recording_options', 'recording_mode')
            if recording_mode == 'press_to_toggle':
                print("Stopping recording (toggle mode)")
                self.result_thread.stop_recording()
            elif recording_mode == 'continuous':
                print("Stopping recording (continuous mode)")
                self.stop_result_thread()
            return

        self.start_result_thread()

    def on_deactivation(self):
        """Called when the activation key combination is released."""
        if ConfigManager.get_config_value('recording_options', 'recording_mode') == 'hold_to_record':
            if self.result_thread and self.result_thread.isRunning():
                print("Stopping recording (hold mode)")
                self.result_thread.stop_recording()

    def start_result_thread(self):
        """Start the result thread to record audio and transcribe it."""
        if self.result_thread and self.result_thread.isRunning():
            return

        print("Starting recording...")
        self.result_thread = ResultThread(self.local_model)
        self.result_thread.resultSignal.connect(self.on_transcription_complete)
        self.result_thread.start()

    def stop_result_thread(self):
        """Stop the result thread."""
        try:
            if self.result_thread and hasattr(self.result_thread, 'isRunning') and self.result_thread.isRunning():
                self.result_thread.stop()
        except Exception as e:
            print(f"Error stopping result thread: {e}")

    def on_transcription_complete(self, result):
        """When transcription is complete, type the result and optionally copy to clipboard."""
        print(f"Transcription complete: {result}")
        
        # Copy to clipboard if enabled
        if ConfigManager.get_config_value('post_processing', 'auto_copy_to_clipboard'):
            try:
                import pyperclip
                pyperclip.copy(result)
                print("Text copied to clipboard")
            except ImportError:
                print("pyperclip not available, skipping clipboard copy")
        
        # Type the text
        print("Typing text...")
        self.input_simulator.typewrite(result)
        
        # Play completion sound if enabled (skip if no audio device)
        if ConfigManager.get_config_value('misc', 'noise_on_completion'):
            try:
                from audioplayer import AudioPlayer
                AudioPlayer(os.path.join('assets', 'beep.wav')).play(block=True)
                print("Played completion sound")
            except Exception as e:
                print(f"Could not play sound: {e}")

        # Handle continuous recording mode
        if ConfigManager.get_config_value('recording_options', 'recording_mode') == 'continuous':
            print("Continuous mode - starting new recording")
            self.start_result_thread()
        else:
            print("Ready for next activation")

    def run(self):
        """Main loop - start key listener and keep running"""
        print("Starting key listener...")
        
        try:
            self.key_listener.start()
            print("WhisperWriter headless mode is running!")
            print(f"Listening for hotkey: {ConfigManager.get_config_value('recording_options', 'activation_key')}")
            print("Press Ctrl+C to exit")
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("Interrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()


if __name__ == '__main__':
    print('Starting WhisperWriter in headless mode...')
    load_dotenv()
    
    app = HeadlessWhisperWriter()
    app.run() 