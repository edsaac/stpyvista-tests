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

pv.global_theme.show_scalar_bar = False

"## 🔑   Pass a key"

## Initialize a plotter object
plotter = pv.Plotter(window_size=[250, 250])

## Create a mesh with a cube
mesh = pv.Cube(center=(0, 0, 0))

## Add some scalar field associated to the mesh
mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)

## Final touches
plotter.view_isometric()

## Show in streamlit
cols = st.columns(2)

with cols[0]:
    "### 🔑 With a key"
    ## Pass a key to the component to avoid remounting it at each Streamlit rerun
    with st.echo(code_location="below"):
        stpyvista(plotter, key="pv_cube")

with cols[1]:
    "### ⭕ Without a key"
    ## Without a key, Streamlit re mounts the whole thing at each interaction :(
    with st.echo(code_location="below"):
        stpyvista(plotter)

st.button("🤔 Will this button make stpyvista to lose its state?")

"****"

st.warning(
    """Code adapted from https://docs.pyvista.org/user-guide/jupyter/pythreejs.html#scalars-support"""
)
