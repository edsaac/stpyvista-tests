import streamlit as st
from stpyvista import stpyvista
import pyvista as pv
import matplotlib as mpl
import numpy as np

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

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
        ## Sample a matplotlib colormap
        colors = cmap(np.linspace(0, 1, N_BOXES))

        ## Add boxes to pyvista plotter
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

        with render_placeholder:
            stpyvista(plotter, panel_kwargs=dict(orientation_widget=True))

###########
"**********"
"## 🛕 Opacity as a field"

cols = st.columns([1.5, 1])

with cols[1]:
    "### 🔅 Opacity from a field"
    code_placeholder = st.empty()
with cols[0]:
    "&nbsp;"
    COLOR_PICK = st.color_picker("`COLOR_PICK`", value="#800080")
    render_placeholder = st.empty()

with code_placeholder:
    with st.echo():
        # Create coordinate data
        x, y = np.arange(-10, 10, 0.25), np.arange(-10, 10, 0.25)
        x, y = np.meshgrid(x, y)
        z = 4 * np.sin(np.sqrt(x**2 + y**2))

        # Initialize plotter
        plotter = pv.Plotter()

        # Add a plane
        plane = pv.Plane(center=[0, 0, -5.2], direction=[0, 0, 1], i_size=25, j_size=25)
        plane.point_data.clear()
        plotter.add_mesh(plane, color="#00FF7F", show_edges=True, edge_color="purple")

        # Add the surface
        surface = pv.StructuredGrid(x, y, z)
        zp = surface.points[:, 2]
        surface["opacity"] = np.interp(zp, [zp.min(), zp.max()], [0.2, 1])
        plotter.add_mesh(surface, color=COLOR_PICK, opacity=surface["opacity"])

        ## Send to streamlit
        plotter.background_color = "white"
        plotter.camera.zoom("tight")
        plotter.view_isometric()
        plotter.window_size = [400, 400]

        with render_placeholder:
            stpyvista(plotter, panel_kwargs=dict(orientation_widget=True))
