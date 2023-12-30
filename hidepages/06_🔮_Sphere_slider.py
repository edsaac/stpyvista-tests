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

"## 🔮 Sphere"

with st.echo(code_location="below"):
    
    import pyvista as pv
    from stpyvista import stpyvista

    res = st.slider("Resolution", 5, 100, 20, 5)

    # Set up plotter
    plotter = pv.Plotter(window_size=[300, 300])

    # Create element
    sphere = pv.Sphere(phi_resolution=res, theta_resolution=res)
    plotter.add_mesh(sphere, name="sphere", show_edges=True)

    plotter.view_isometric()
    plotter.set_background("white")

    # Pass the plotter (not the mesh) to stpyvista
    stpyvista(plotter)

    "****"
