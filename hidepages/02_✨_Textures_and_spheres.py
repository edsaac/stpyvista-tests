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
"## ✨   Textures and spheres"

st.error("Textures in Panel are not rendered?")

placeholder_render = st.empty()

with st.expander("See code:", expanded=False):
    with st.echo():

        @st.cache_resource
        def stpv_spheres(dummy:str = "spheres"):
            colors = ["red", "teal", "black", "orange", "silver"]
            plotter = pv.Plotter(border=False, window_size=[600, 400])
            plotter.background_color = "white"

            # Add a bunch of spheres with different properties
            for i in range(5):
                for j in range(6):
                    sphere = pv.Sphere(radius=0.5, center=(0.0, 4 - i, j))
                    plotter.add_mesh(
                        sphere, color=colors[i], pbr=True, metallic=i / 4, roughness=j / 5
                    )

            plotter.view_vector((-1, 0, 0), (0, 1, 0))
            plotter.camera.zoom(1.5)
            return plotter
        
        # Send to streamlit
        with placeholder_render:
            stpyvista(stpv_spheres(), key="pvSpheres")

st.warning("Code adapted from https://docs.pyvista.org/examples/02-plot/pbr.html")
