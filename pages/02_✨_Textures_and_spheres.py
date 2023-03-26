import pyvista as pv
import streamlit as st
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

st.title("✨   Textures and spheres")

st.error("Textures in Panel are not rendered?")

placeholder_render = st.empty()

with st.expander("See code:", expanded=False):
    with st.echo():
        colors = ['red', 'teal', 'black', 'orange', 'silver']
        
        ## Initialize pyvista reader and plotter
        plotter = pv.Plotter(border=False, window_size=[600,400]) 
        plotter.background_color = "white"
        
        ## Add a bunch of spheres with different properties
        for i in range(5):
            for j in range(6):
                sphere = pv.Sphere(radius=0.5, center=(0.0, 4 - i, j))
                plotter.add_mesh(sphere, color=colors[i], pbr=True, metallic=i / 4, roughness=j / 5)
        
        plotter.view_vector((-1, 0, 0), (0, 1, 0))
        plotter.camera.zoom(1.5)
        
        ## Send to streamlit
        with placeholder_render:
            stpyvista(plotter, key="pvSpheres")

st.warning("""
Code adapted from https://docs.pyvista.org/examples/02-plot/pbr.html
""")