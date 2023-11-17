import pyvista as pv

# pv.start_xvfb()

import streamlit as st
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

if "sphere" not in st.session_state:
    pl = pv.Plotter(window_size=[300, 200])
    pl.set_background("#D3EEFF")
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    pl.view_isometric()
    st.session_state.sphere = pl

sphere = st.session_state.sphere

"## 📐   Horizontal alignment"
alignment = st.select_slider("Align", ["left", "center", "right"], label_visibility="collapsed")
stpyvista(sphere, horizontal_align=alignment, use_container_width=False)
