import pyvista as pv
import streamlit as st
from stpyvista import stpyvista
from stpyvista_utils import is_embed, is_xvfb
import matplotlib as mpl
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

"## 🏯 Opacity"
cmap = mpl.cm.tab20c_r
cols = st.columns([2, 1])

with cols[0]:
    "### 🔅 Single opacity value per mesh"
    code_placeholder = st.empty()

with cols[1]:
    "&nbsp;"
    N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)
    render_placeholder = st.empty()

with code_placeholder:
    with st.echo():
        
        ## Add boxes to pyvista plotter
        @st.cache_resource
        def stpv_tower(n_boxes:int):
            ## Sample a matplotlib colormap
            colors = cmap(np.linspace(0, 1, n_boxes))

            plotter = pv.Plotter()
            for i, c in enumerate(colors, start=1):
                cube = pv.Cube(center=(0, 0, i), x_length=2.5, y_length=1.5, z_length=0.75)
                cube = cube.rotate_z(i * 90 / 15, point=(0, 0, 0), inplace=True)
                plotter.add_mesh(
                    cube, edge_color="black", color=c, opacity=i / N_BOXES, show_edges=True
                )

            ## Plotter configuration
            plotter.background_color = "#ffffff"
            plotter.camera.zoom("tight")
            plotter.view_isometric()
            plotter.window_size = [200, 400]
            return plotter
        
        tower = stpv_tower(N_BOXES)

        with render_placeholder:
            stpyvista(tower, panel_kwargs=dict(orientation_widget=True))

###########
"**********"
"## 🛕 Opacity as a field"

cols = st.columns([1.5, 1])

with cols[1]:
    "### 🔅 Opacity from a field"
    code_placeholder = st.empty()
with cols[0]:
    "&nbsp;"
    COLOR_PICK = st.color_picker("`COLOR_PICK`", value="#800080", help="Pick a color for the plane")
    render_placeholder = st.empty()

with code_placeholder:
    with st.echo():
        @st.cache_resource
        def stpv_ripple(dummy:str = "ripple"):
            # Create coordinate data
            x, y = np.arange(-10, 10, 0.25), np.arange(-10, 10, 0.25)
            x, y = np.meshgrid(x, y)
            z = 4 * np.sin(np.sqrt(x**2 + y**2))

            # Initialize plotter
            plotter = pv.Plotter()

            # Add a plane
            plane = pv.Plane(center=[0, 0, -5.2], direction=[0, 0, 1], i_size=25, j_size=25)
            plane.point_data.clear()
            plotter.add_mesh(plane, color="#00FF7F", show_edges=True, edge_color="purple", name="plane")

            # Add the surface
            surface = pv.StructuredGrid(x, y, z)
            zp = surface.points[:, 2]
            surface["opacity"] = np.interp(zp, [zp.min(), zp.max()], [0.2, 1])
            plotter.add_mesh(
                surface,
                color="#ff0000",
                opacity=surface["opacity"],
                show_scalar_bar=False,
                name="ripple"
            )

            ## Send to streamlit
            plotter.background_color = "#ffffff"
            plotter.camera.zoom("tight")
            plotter.view_isometric()
            plotter.window_size = [400, 400]
            return plotter
        
        ripple = stpv_ripple()
        ripple.actors['plane'].prop.color = COLOR_PICK 

        with render_placeholder:
            stpyvista(ripple, panel_kwargs=dict(orientation_widget=True))
