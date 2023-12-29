import streamlit as st
from stpyvista import stpyvista
from stpyvista_utils import is_embed, is_xvfb
import geovista as gv
import numpy as np

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

"## 🌎 Running `geovista` for cartographic rendering"

@st.cache_resource
def stpv_planet(dummy:str = "planet"):
    from collections import namedtuple
    Point = namedtuple("Point", ["lat", "lon"])

    x = np.arange(-180, 182, 2) #Lon
    y = np.arange(90, -92, -2)  #Lat
    xx,yy = np.meshgrid(
        np.deg2rad(x), 
        np.deg2rad(y)
    )

    p = Point(np.deg2rad(4.60971), np.deg2rad(-74.08175)) # Bogotá
    radius = 6_371 # Radius earth

    # "d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)])"
    
    # data = np.abs(yy)
    data = 2 * radius * np.arcsin(
        np.sin((yy - p.lat)/2)**2 +
        np.cos(p.lat) * np.cos(yy) * np.sin((xx - p.lon)/2)**2
    )

    blob = gv.Transform.from_1d(
        x,y, data=data, name="Distance to Bogota [km]"
    )

    plotter = gv.GeoPlotter()
    plotter.window_size = [450, 450]
    plotter.background_color = "#080D35"
    plotter.add_graticule(
        lon_step=10,
        lat_step=10,
        mesh_args=dict(
            color="pink",
            opacity=0.2,
        )
    )
    plotter.add_coastlines(
        color="white", 
        line_width=12
    )
    plotter.view_xz(negative=False)
    plotter.add_text(
        "🌎 Distance to Bogotá",
        position="upper_left",
        color="w",
        font_size=15,
        shadow=True,
    )

    plotter.add_text(
        "▛ geovista ▟",
        position="lower_edge",
        color="pink",
        font_size=12,
        shadow=True,
    )

    plotter.add_mesh(
        blob, show_edges=False, 
        style='surface', cmap="CET_R1_r",
        clim=[0, np.pi * radius]
    )

    return plotter

planet = stpv_planet()

stpyvista(
    planet,
    panel_kwargs=dict(
        orientation_widget=True, 
        interactive_orientation_widget=True
    )
)


with st.sidebar:
    
    st.info(
        "Check another example at [`geovista.streamlit.app`](https://geovista.streamlit.app/)"
        " and visit the [`geovista`](https://github.com/bjlittle/geovista) project."
    )
