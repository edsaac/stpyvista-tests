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

"## 🔑   Pass a key"
# pv.global_theme.show_scalar_bar = False

## Initialize a plotter object
@st.cache_resource
def stpv_key(dummy:str = "key"):
    plotter = pv.Plotter(window_size=[250, 250])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
    plotter.view_isometric()
    return plotter

plotter = stpv_key()

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
