import logging
import streamlit as st
from textwrap import wrap
from typing import Callable

from stpyvista import stpyvista
from pantry.utils import start_xvfb
import pantry.stpyvista_pantry as stpv
from pantry.webapp_fragments import (
    gallery,
    fill_up_main_window,
)

gallery: dict[str, Callable]

# Hide param warnings
logging.getLogger("param.main").setLevel(logging.CRITICAL)

# Initial configuration
if "xvfb" not in st.session_state:
    st.session_state["xvfb"] = start_xvfb()

# print(f"--> IP: {st.context.ip_address or 'Not-found'}")


def main():
    st.set_page_config(
        page_title="stpyvista · Show 3D visualizations from PyVista in Streamlit",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={"About": "Last updated Oct/20/25"},
    )
    
    # Add styling with CSS selectors
    st.html("assets/style.css")

    # --------------------------------------------
    # Full version
    # --------------------------------------------
    # General layout
    with st.sidebar:
        side_title_container = st.empty()
        "****"
        side_gallery_container = st.container()
        "****"
        side_other_container = st.empty()

    main_container = st.empty()

    # Figure out section
    selection_from_query = st.query_params.get("gallery", None)

    if selection_from_query in gallery.keys():
        st.session_state["gallery_select"] = selection_from_query

    with side_gallery_container:
        st.subheader("Gallery", anchor=False)

        selection = st.pills(
            "Gallery selection",
            gallery.keys(),
            selection_mode="single",
            default=None,
            format_func=lambda x: "\n\n".join(wrap(gallery[x].__doc__, 12)),
            label_visibility="collapsed",
            on_change=st.query_params.clear,
            key="gallery_select",
        )

        selection = selection_from_query or selection

    # Add badges and other info to sidebar
    with side_other_container.container():
        st.subheader("Useful links", anchor=False)
        st.html("assets/badges.html")
    
    # --- Initial page - no selection from gallery -----
    if not selection:
        with side_title_container.container():
            st.title("[🧊](https://github.com/edsaac/stpyvista)", anchor=False)
            st.caption(
                """
                [`stpyvista`](https://github.com/edsaac/stpyvista) displays PyVista 
                plotter objects in streamlit web apps using 
                [`panel`](https://panel.holoviz.org/reference/panes/VTK.html) and
                [`trame`](https://github.com/Kitware/trame)
                """
            )

        with main_container.container(horizontal_alignment="center"):
            st.header("`stpyvista`", anchor="stpyvista")
            st.subheader("Show PyVista 3D visualizations in Streamlit", anchor=False)

            ## Send plotter to streamlit
            plotter = stpv.intro()
            stpyvista(
                plotter,
                backend="panel",
                backend_kwargs=dict(
                    orientation_widget=True,
                    interactive_orientation_widget=True,
                ),
            )

            st.info("Check the examples gallery in the sidebar!", icon="👈")

            fill_up_main_window()

    # --- Other pages - with selection from gallery -----
    else:
        with side_title_container.container(horizontal_alignment="center"):
            st.header(
                """[🧊 `stpyvista`](https://stpyvista.streamlit.app)""",
                anchor=False,
            )

        main_container.empty()
        st.query_params["gallery"] = selection

        with main_container.container():
            gallery[selection]()
    
            with st.container(border=True):
                lcol, rcol = st.columns([1, 3], vertical_alignment="center")
                lcol.write("📦 &nbsp; :green-background[**Install:**]")
                rcol.code("pip install stpyvista", language="sh")
                


if __name__ == "__main__":
    main()
