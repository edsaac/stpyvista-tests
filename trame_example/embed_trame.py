import streamlit as st
import shlex
from subprocess import Popen
import atexit


def launch_trame(path_script: str):
    command = f"python {path_script} --port 1234"
    args = shlex.split(command)
    p = Popen(args)
    return p


def close_trame(p: Popen):
    print("Closing trame")
    p.terminate()


def main():
    "# Trame within streamlit"

    p = launch_trame("solution_cone.py")
    atexit.register(close_trame, p)

    st.components.v1.iframe("http://localhost:1234", height=400)


if __name__ == "__main__":
    main()
