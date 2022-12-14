import pyvista as pv
import streamlit as st
from stpyvista import stpyvista
pv.global_theme.show_scalar_bar = False

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)


def get_cow():
    return pv.examples.download_cow()

st.title("🔁 Rotate around axis")

## Some controls
with st.form("Controls"):
    axis = st.radio("Axis of rotation", [*"xyz"], horizontal=True)
    speed = st.slider("Rotation speed", 0.1, 2.0, 0.2, 0.1, "%.1f")
    st.form_submit_button("Submit")

## Initialize a plotter object
plotter = pv.Plotter(window_size=[600,500])

cow = get_cow()
plotter.add_mesh(cow)
plotter.view_xy()

## Create animation
rotation = {"axis":axis, "revolution_time":1/speed}
stpyvista(plotter, rotation=rotation)

