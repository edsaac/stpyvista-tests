import pyvista as pv
import streamlit as st
from stpyvista import stpyvista
from stpyvista_utils import is_embed, is_xvfb
import matplotlib as mpl
import numpy as np
from itertools import product
from random import random

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

"## 🪓 Axes"

with st.sidebar:
    st.info(
        """
        Check `panel` documentation for more options
        https://panel.holoviz.org/api/panel.pane.vtk.html
        """
    )

"### Axes configuration using `panel.pane.vtk`"

with st.expander("🪓 **Documentation**"):
    f"""
    Source: [panel.holoviz.org](https://panel.holoviz.org/api/panel.pane.vtk.html#panel.pane.vtk.vtk.AbstractVTK)

    `axes` is a dictionary containing the parameters of the axes to
    construct in the 3d view. It **must contain** at least `xticker`,
    `yticker` and `zticker`.

    A *ticker* is a dictionary which contains:
    - `ticks` : List[float] - required.
        > Positions in the scene coordinates of the corresponding
        > axis' ticks.
    - `labels` : List[str] - optional.
        > Label displayed respectively to the `ticks` positions.
        > If `labels` are not defined, they are inferred from the
        > `ticks` array.

    Other optional parameters for `axes` are:
    - `digits`: int
        > number of decimal digits when `ticks` are converted to `labels`.
    - `fontsize`: int
        > size in pts of the ticks labels.
    - `show_grid`: bool = True
        > If true the axes grid is visible.
    - `grid_opacity`: float between 0-1.
        > Defines the grid opacity.
    - `axes_opacity`: float between 0-1.
        > Defines the axes lines opacity.

    """

## Add boxes to pyvista plotter
@st.cache_resource
def stpv_axis(dummy:str = "axis"):
    cmap = mpl.cm.hsv
    plotter = pv.Plotter()

    for i, j, k in product([1, 2, 3], repeat=3):
        sphere = pv.Sphere(radius=0.25, center=(i, j, k))
        plotter.add_mesh(sphere, color=cmap(random()), opacity=0.5)

    ## Plotter configuration
    plotter.background_color = "#ffffee"
    plotter.view_isometric()
    plotter.camera.elevation = -10
    plotter.camera.azimuth = 20
    plotter.window_size = [550, 500]
    return plotter

with st.echo("below"):
    # Define axes to put in the rendered view
    axes = dict(
        ## tickers are required, one for each axis
        xticker=dict(
            ticks=[0, 1, 2, 3, 4],  ## ticks are required
            labels=["", "😎", "DOS", "🌺", "IV"],
        ),
        yticker=dict(
            ticks=[0, 1, 2, 3, 4],  ## <- This needs to be a python list, not a np.array
            labels=[*" αβγδ"],  ## labels are optional
        ),
        zticker=dict(
            ticks=np.arange(0, 5, 1).tolist()
        ),
        ## Optional parameters
        origin=[0, 0, 0],
        fontsize=22,
        show_grid=True,
        grid_opacity=0.1,
        axes_opacity=1.0,
        digits=1,
    )

    # Pass those axes to panel_kwargs of stpyvista
    plotter = stpv_axis()
    stpyvista(plotter, panel_kwargs=dict(axes=axes, orientation_widget=True))
