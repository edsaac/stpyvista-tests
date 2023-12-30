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
"## 📐   Horizontal alignment"

@st.cache_resource
def stpv_sphere(dummy:str = "sphere"):
    pl = pv.Plotter(window_size=[300, 200])
    pl.set_background("#D3EEFF")
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    pl.view_isometric()
    return pl

alignment = st.select_slider(
    "Align", 
    ["left", "center", "right"], 
    label_visibility="collapsed"
)

stpyvista(
    stpv_sphere(), 
    horizontal_align=alignment, 
    use_container_width=False
)
