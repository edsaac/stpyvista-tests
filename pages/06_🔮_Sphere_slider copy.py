import streamlit as st

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

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
