import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

if "sphere" not in st.session_state:
    pl = pv.Plotter(window_size=[300,200])
    pl.set_background('#D3EEFF')
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    st.session_state.sphere = pl

sphere = st.session_state.sphere

st.title("📐   Horizontal alignment")

with st.echo():
    # The default is centered
    stpyvista(sphere, key="sphere_center")

with st.echo():
    # But it can go on the left
    stpyvista(sphere, horizontal_align="left", key="sphere_left")

with st.echo():
    # Or on the right
    stpyvista(sphere, horizontal_align="right", key="sphere_right")