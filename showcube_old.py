import numpy as np
import pyvista as pv
import streamlit as st
from stpyvista import stpyvista, HTML_stpyvista


pv.global_theme.show_scalar_bar = False

st.title("A cube")

st.info("""
Code adapted from https://docs.pyvista.org/user-guide/jupyter/pythreejs.html#scalars-support
""")

if "model" not in st.session_state:    
    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400,400])

    ## Create a mesh with a cube 
    mesh = pv.Cube(center=(0,0,0))

    ## Add some scalar field associated to the mesh
    mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

    ## Add mesh to the plotter
    plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

    ## Final touches
    plotter.view_isometric()
    plotter.background_color = 'white'
    
    ## Export and save to st.session_state
    st.session_state.model = HTML_stpyvista(plotter)

stpyvista(st.session_state.model)
st.button("Restart?")