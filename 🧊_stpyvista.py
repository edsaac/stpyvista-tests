import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

if "carburator" not in st.session_state:
    st.session_state.carburator = pv.examples.download_carburator()

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

st.title("🧊 `stpyvista`")
st.header("Show PyVista 3D visualizations in Streamlit")

cols = st.columns([1,1])

with cols[0]:
    st.markdown("""
    `stpyvista` is a simple component that takes a PyVista plotter object and shows 
    it on Streamlit as an interactive element (as in it can be zoomed in/out, moved 
    and rotated, but the visualization state is not returned).
    It uses PyVista's [pythreejs backend](https://docs.pyvista.org/user-guide/jupyter/pythreejs.html) 
    and it basically takes the plotter, [exports it to HTML](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.export_html.html) 
    and displays that within an iframe.

    **👈 List of demos:**

    - 🔑   Pass a key to avoid model re-rendering
    - 🍞   Textures and physically based rendering (PBR)
    - 📤   Display your own STL file

    ****
    """, unsafe_allow_html=True)

with cols[1]:

    pl_carburator = pv.Plotter(window_size=[400,300])
    pl_carburator.set_background('white')
    st.session_state.carburator.decimate(0.5, inplace=True)
    pl_carburator.add_mesh(st.session_state.carburator, color='lightgrey', pbr=True, metallic=0.5)
    pl_carburator.camera.zoom(1.5)
    stpyvista(pl_carburator, horizontal_align="right", key="pv_carburator")

with st.expander("🛠️ Installation"):
    """
    ```sh
    pip install stpyvista
    ```
    """

with st.expander("✨ Use example", expanded=True):

    with st.echo():
        import streamlit as st
        import pyvista as pv
        from stpyvista import stpyvista
        
        # ipythreejs does not support scalar bars :(
        pv.global_theme.show_scalar_bar = False 

        ## Initialize a plotter object
        plotter = pv.Plotter(window_size=[400,400])

        ## Create a mesh with a cube 
        mesh = pv.Cube(center=(0,0,0))

        ## Add some scalar field associated to the mesh
        mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

        ## Add mesh to the plotter
        plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

        ## Final touches
        plotter.view_isometric()
        plotter.background_color = 'white'

        ## Pass a key to avoid re-rendering at each time something changes in the page
        stpyvista(plotter, key="pv_cube")

with st.expander("🔡 Also check:"):
    """
    * The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
    * @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component
    * [Post](https://discuss.streamlit.io/t/stpyvista-show-pyvista-3d-visualizations-in-streamlit/31802) on streamlit discuss forum.

    """