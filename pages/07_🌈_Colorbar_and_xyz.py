import streamlit as st
from stpyvista import stpyvista
import pyvista as pv

st.set_page_config(page_icon="🧱", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

"## 🌈 Colorbar and orientation widget"

plotter = pv.Plotter(window_size=[400, 400])
mesh = pv.Cube(center=(0, 0, 0))
mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
plotter.background_color = "white"
plotter.view_isometric()
plotter.add_title("Cute cube", color="black", font_size=16)

"### 🌈 The three dots expand the colorbar legend"
with st.echo():
    stpyvista(plotter)

"****"
"### 🧭 Orientation widget: xyz directions"
with st.echo():
    stpyvista(plotter, panel_kwargs=dict(orientation_widget=True))

"****"
"### 🖱️ Make the orientation widget interactive "
with st.echo():
    stpyvista(
        plotter,
        panel_kwargs=dict(orientation_widget=True, interactive_orientation_widget=True),
    )

with st.sidebar:
    st.info(
        """Check the 
        [`panel`](https://panel.holoviz.org/reference/panes/VTK.html) 
        documentation for VTK to find other `panel_kwargs` than could be 
        passed to `stpyvista`. """
    )
