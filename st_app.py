import streamlit as st
import pyvista as pv
from stpyvista import stpyvista
import subprocess
import urllib.parse as parse

def is_embed():
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    ctx = get_script_run_ctx()
    query_params = parse.parse_qs(ctx.query_string)
    return True if query_params.get("embed") else False

IS_APP_EMBED = is_embed()

st.set_page_config(
    page_title="stpyvista",
    page_icon="🧊", 
    layout="wide" if IS_APP_EMBED else "centered", 
    initial_sidebar_state="collapsed" if IS_APP_EMBED else "expanded")

## Check if xvfb is already running on the machine
is_xvfb_running = subprocess.run(["pgrep", "Xvfb"], capture_output=True)

if is_xvfb_running.returncode == 1:
    if not IS_APP_EMBED:
        st.toast("Xvfb was not running...", icon="⚠️")
    pv.start_xvfb()
else:
    if not IS_APP_EMBED:
        st.toast(f"Xvfb is running! \n\n`PID: {is_xvfb_running.stdout.decode('utf-8')}`", icon="📺")

# @st.cache_data
# def get_cow(does_nothing="cow"):
#     with open("assets/cow.pkl", "rb") as f:
#         cow = pickle.load(f)
#         print(type(cow))
#     return cow

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Add badges to sidebar
if not IS_APP_EMBED:
    with st.sidebar:
        with open("assets/badges.md") as f:
            st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

st.title("🧊 `stpyvista`")
st.subheader("Show PyVista 3D visualizations in Streamlit")

## Pyvista code
cow = pv.Cylinder(radius=3.5, height=8)
nose = pv.Cylinder(radius=0.5, height=8, direction=(0, 0, 1), center=(0, 0, 1.7))
eye_left = pv.Cylinder(radius=1.0, height=4, direction=(0, 0, 1), center=(-2.0, 1, 2))
eye_left_p = pv.Cylinder(radius=0.3, height=4.1, direction=(0, 0, 1), center=(-2.0, 1, 2))
eye_right = pv.Cylinder(radius=1.0, height=4, direction=(0, 0, 1), center=(2.0, 1, 2))
eye_right_p = pv.Cylinder(radius=0.3, height=4.1, direction=(0, 0, 1), center=(2.0, 1, 2))


plotter = pv.Plotter()

plotter.add_mesh(cow, color="grey", pbr=True, metallic=0.05)
plotter.add_mesh(nose, color="red", pbr=True, metallic=0.05)
plotter.add_mesh(eye_left, color="white", pbr=True, metallic=0.05)
plotter.add_mesh(eye_right, color="white", pbr=True, metallic=0.05)
plotter.add_mesh(eye_left_p, color="green")
plotter.add_mesh(eye_right_p, color="green")


plane = pv.Plane(center=[0, -3.65, 0], direction=[0, 1, 0], i_size=12, j_size=12)
plotter.add_mesh(plane, color="#09ab3b", show_edges=True)

# plotter.add_floor('-y', show_edges=True, color="#09ab3b", opacity=0.8)

## Send to streamlit
plotter.background_color = "white"
plotter.view_xy()
plotter.camera.azimuth = 25
plotter.camera.elevation = 15

plotter.window_size = [450, 300]
stpyvista(plotter, horizontal_align="center",
    panel_kwargs=dict(orientation_widget=True, interactive_orientation_widget=True)
)

"""
`stpyvista` is a simple component that takes a PyVista plotter object and shows 
it on Streamlit as an interactive element (as in it can be zoomed in/out, moved 
and rotated, but the visualization state is not returned).
It uses PyVista's [panel backend](https://docs.pyvista.org/user-guide/jupyter/panel.html) 
for taking the plotter, [exports it to HTML](https://panel.holoviz.org/reference/panes/VTK.html) 
and displays that within an iframe.

**👈 Check the list of demos**
****
"""

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

        ## Initialize a plotter object
        plotter = pv.Plotter(window_size=[400, 400])

        ## Create a mesh with a cube
        mesh = pv.Cube(center=(0, 0, 0))

        ## Add some scalar field associated to the mesh
        mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]

        ## Add mesh to the plotter
        plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)

        ## Final touches
        plotter.background_color = "white"
        plotter.view_isometric()

        ## Pass a key to avoid re-rendering at each time something changes in the page
        stpyvista(plotter, key="pv_cube")

with st.expander("🔡 Also check:"):
    """
    * The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
    * Holoviz Panel VTK at [https://panel.holoviz.org/](https://panel.holoviz.org/reference/panes/VTK.html)
    * @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component
    * [Post](https://discuss.streamlit.io/t/stpyvista-show-pyvista-3d-visualizations-in-streamlit/31802) on streamlit discuss forum.

    """

r"""
*****
Current version **0.0.8**
"""
