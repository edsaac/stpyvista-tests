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

"## 🌈 Colorbar and orientation widget"

st.info("""
    Colorbars bug has been fixed in panel 1.3.2.
    - More info: https://github.com/holoviz/panel/releases/tag/v1.3.2
    - To upgrade: `pip install panel -U`
""")

@st.cache_resource
def stpv_cube(dummy:str = "cube"):
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
    plotter.background_color = "white"
    plotter.view_isometric()
    plotter.add_title("◱ Check the corners ◲", color="purple", font_size=20)
    return plotter

cube = stpv_cube()    

"### 🌈 The three dots expand the colorbar legend"
with st.echo():
    stpyvista(cube)

"****"
"### 🧭 Orientation widget: xyz directions"
with st.echo():
    stpyvista(cube, panel_kwargs=dict(orientation_widget=True))

"****"
"### 🖱️ Make the orientation widget interactive "
with st.echo():
    stpyvista(
        cube,
        panel_kwargs=dict(
            orientation_widget=True, 
            interactive_orientation_widget=True
        ),
    )

with st.sidebar:
    st.info(
        """Check the 
        [`panel`](https://panel.holoviz.org/reference/panes/VTK.html) 
        documentation for VTK to find other `panel_kwargs` than could be 
        passed to `stpyvista`. """
    )
