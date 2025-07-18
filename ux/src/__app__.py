import subprocess
import os
import signal
import sys

def run():
    """Main Streamlit app function"""
    try:
        app_path = os.path.join(os.path.dirname(__file__), 'app.py')
        
        # Create the subprocess
        process = subprocess.Popen(
            ["uv", "tool", "run", "streamlit", "run", app_path],
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )
        
        def signal_handler(signum, frame):
            """Handle Ctrl+C signal"""
            print("\nShutting down Streamlit...")
            try:
                if hasattr(os, 'killpg'):
                    # Kill the entire process group (Unix/macOS)
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                else:
                    # Fallback for systems without process groups
                    process.terminate()
                process.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                # Force kill if graceful shutdown fails
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                else:
                    process.kill()
            sys.exit(0)
        
        # Register signal handler for Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Wait for the process to complete
        process.wait()
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to run the Streamlit app: {e}")
    except KeyboardInterrupt:
        print("\nStreamlit app interrupted by user")
        sys.exit(0)