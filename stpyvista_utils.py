import subprocess
import urllib.parse as parse
from pyvista import start_xvfb
from collections import namedtuple

def is_embed():
    """Check if the app is embed"""
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    ctx = get_script_run_ctx()
    query_params = parse.parse_qs(ctx.query_string)
    return True if query_params.get("embed") else False

def is_xvfb():
    """Check if xvfb is already running on the machine"""

    State = namedtuple("State", ["status", "message", "icon"])
    is_xvfb_running = subprocess.run(["pgrep", "Xvfb"], capture_output=True)

    if is_xvfb_running.returncode == 1:
        start_xvfb()
        return State(False, "Xvfb was not running...", "⚠️")
    
    elif is_xvfb_running.returncode == 0:
        return State(
            True, 
            f"Xvfb is running! \n\n`PID: {is_xvfb_running.stdout.decode('utf-8')}`",
            "📺")
    
    else:
        return State(False, "Something went wrong", "❌")

    
def main():
    pass

if __name__ == "__main__":
    main()