import subprocess
import urllib.parse as parse
from pyvista import start_xvfb
from collections import namedtuple
from streamlit import runtime

from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web.server.websocket_headers import _get_websocket_headers

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
            f"Xvfb is running!: \t `PID: {is_xvfb_running.stdout.decode('utf-8').strip()}`",
            "📺",
        )

    else:
        return State(False, "Something went wrong", "❌")


def get_ip():
    
    # https://github.com/streamlit/streamlit/issues/602#issuecomment-1872464455

    headers = _get_websocket_headers()

    if headers is not None:
        x_forwarded_for = headers.get('X-Forwarded-For', None)
        origin = headers.get('Origin', None)

        return x_forwarded_for or origin or "__not_found__"
    
    return "__not_found__"


def main():
    pass


if __name__ == "__main__":
    main()
