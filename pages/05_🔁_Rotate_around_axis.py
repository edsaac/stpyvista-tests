import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

pv.global_theme.show_scalar_bar = False

@st.experimental_singleton
def get_cow():
    return pv.examples.download_cow()

st.title("🔁 Rotate around axis")

## Initialize a plotter object
plotter = pv.Plotter(window_size=[600,500])

cow = get_cow()
plotter.add_mesh(cow)
plotter.view_xy()

## Create animation
rotation = {"axis":'y', "revolution_time":3.0}
stpyvista(plotter, rotation=rotation ,key="pv_cow")

