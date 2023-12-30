import pyvista as pv
import streamlit as st
from stpyvista import stpyvista
from stpyvista_utils import is_embed, is_xvfb

# Initial configuration
if "IS_APP_EMBED" not in st.session_state:
    st.session_state.IS_APP_EMBED = is_embed()
IS_APP_EMBED = st.session_state.IS_APP_EMBED

if "IS_XVFB_RUNNING" not in st.session_state:
    st.session_state.IS_XVFB_RUNNING = is_xvfb()
IS_XVFB_RUNNING = st.session_state.IS_XVFB_RUNNING

st.set_page_config(
    page_title="stpyvista",
    page_icon="🧊", 
    layout="wide" if IS_APP_EMBED else "centered", 
    initial_sidebar_state="collapsed" if IS_APP_EMBED else "expanded")

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Add badges to sidebar
if not IS_APP_EMBED:
    with st.sidebar:
        with open("assets/badges.md") as f:
            st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

#--------------------------------------------------------------------------

"## 🧱 Structured grid"

with st.echo(code_location="below"):
    import pyvista as pv
    import numpy as np
    from stpyvista import stpyvista

    # Set up plotter
    @st.cache_resource
    def stpv_structuredgrid(dummy:str = "grid"):
        # Create coordinate data
        x = np.arange(-10, 10, 0.5)
        y = np.arange(-10, 10, 0.5)
        x, y = np.meshgrid(x, y)
        z = np.sin(np.sqrt(x**2 + y**2))

        plotter = pv.Plotter()
        surface = pv.StructuredGrid(x, y, z)
        plotter.add_mesh(surface, color="pink", show_edges=True, edge_color="k")
        plotter.background_color = "white"
        plotter.view_isometric()
        plotter.window_size = [600, 400]
        return plotter

    # Pass the plotter (not the mesh) to stpyvista
    stpyvista(stpv_structuredgrid(), key="stpv_grid")
