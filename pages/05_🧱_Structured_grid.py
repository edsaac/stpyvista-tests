import streamlit as st

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

"## 🧱 Structured grid"

with st.echo(code_location="below"):
    import pyvista as pv
    import numpy as np
    from stpyvista import stpyvista

    # Create coordinate data
    x = np.arange(-10, 10, 0.5)
    y = np.arange(-10, 10, 0.5)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))

    # Set up plotter
    plotter = pv.Plotter()
    surface = pv.StructuredGrid(x, y, z)
    plotter.add_mesh(surface, color="pink", show_edges=True, edge_color="k")

    # Final touches
    plotter.background_color = "white"
    plotter.view_isometric()
    plotter.window_size = [600, 400]

    # Pass the plotter (not the mesh) to stpyvista
    stpyvista(plotter)
