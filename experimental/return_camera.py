import asyncio
import streamlit as st
import pyvista as pv

from stpyvista import experimental_vtkjs
from stpyvista.export import export_vtksz

@st.cache_resource
def create_plotter(dummy:str = "sphere"):
    
    # Initialize a plotter object
    plotter = pv.Plotter()
    mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))
    
    x, y, z = mesh.cell_centers().points.T
    mesh["My scalar"] = z

    ## Add mesh to the plotter
    plotter.add_mesh(
        mesh,
        scalars="My scalar",
        cmap="prism",
        show_edges=True,
        edge_color="#001100",
        ambient=0.2,
        show_scalar_bar = False
    )
        
    ## Some final touches
    plotter.view_isometric()
    plotter.background_color = "pink"
    
    return plotter

async def main():

    st.set_page_config(
        page_icon="🧊",
        page_title="stpyvista | experimental_vtkjs",
        initial_sidebar_state='collapsed', 
        layout="wide",
    )

    if "css" not in st.session_state:
        with open("./experimental/return_camera.css") as css:
            st.session_state.css = css.read()
    
    plotter = create_plotter()

    if "data" not in st.session_state:
        st.session_state.data = await export_vtksz(plotter)
    
    st.title("🧊 `stpyvista`")
    lcol, rcol = st.columns(2)

    with rcol:
        "🌎 3D Model"
        camera = experimental_vtkjs(st.session_state.data, key="experimental-stpv")
        
    with lcol:
        st.write("*Show PyVista 3D visualizations in Streamlit*")
        
        "🎥 Camera"
        if camera == 0:
            st.info("Interact with the 3D model and you will see here the current camera view")
        else:
            st.json(camera)

    st.html(f"<style>{st.session_state.css}</style>")

if __name__ == "__main__":
    asyncio.run(main())