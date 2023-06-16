import streamlit as st
from stpyvista import stpyvista
import pyvista as pv

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

"## 🏯 Opacity"

## Initialize a plotter object
plotter = pv.Plotter(window_size=[300,600])

## Create a mesh with a cube 

for i in range(1, 11):
    cube = pv.Cube(center=(0, 0, i), x_length=2, y_length=2, z_length=0.8)
    plotter.add_mesh(cube, edge_color='black', color='purple', opacity=i/10, show_edges=True)

## Final touches
plotter.background_color = '#dddddd'
plotter.view_isometric()

## Send to streamlit
stpyvista(plotter, horizontal_align='center')