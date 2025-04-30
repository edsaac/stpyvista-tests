import logging
import streamlit as st
from textwrap import wrap

from stpyvista import stpyvista
from stpyvista.utils import start_xvfb
import pantry.stpyvista_pantry as stpv
from pantry.webapp_fragments import (
    gallery,
    fill_up_main_window,
    fill_install_instructions,
)

# Hide param warnings
logging.getLogger("param.main").setLevel(logging.CRITICAL)

# Initial configuration
# start_xvfb()
print(f"--> IP: {st.context.ip_address or 'Not-found'}")


def main():
    st.set_page_config(
        page_title="stpyvista · Show 3D visualizations from PyVista in Streamlit",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="auto",
    )

    # Add styling with CSS selectors
    with open("assets/style.css") as f:
        st.html(f"""<style>{f.read()}</style>""")

    if st.context.is_embedded:
        with open("assets/style_embed.css") as f:
            st.html(f"""<style>{f.read()}</style>""")

    # --------------------------------------------
    # Full version
    # --------------------------------------------
    if not st.context.is_embedded:
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

        with side_other_container.container():
            # Add badges to sidebar
            with open("assets/badges.html") as f:
                st.subheader("Useful links", anchor=False)
                st.html(f"""{f.read()}""")

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

            with main_container.container():
                st.header("`stpyvista`", anchor="stpyvista")
                st.subheader("Show PyVista 3D visualizations in Streamlit", anchor=False)

                ## Send plotter to streamlit
                plotter = stpv.intro()
                stpyvista(
                    plotter,
                    panel_kwargs=dict(
                        orientation_widget=True,
                        interactive_orientation_widget=True,
                    ),
                    bokeh_resources="CDN",
                )

                st.info("Check the examples gallery in the sidebar!", icon="👈")

                fill_install_instructions()
                fill_up_main_window()

        # *************************************

        else:
            with side_title_container.container():
                st.header(
                    """[🧊 `stpyvista`](https://stpyvista.streamlit.app)""",
                    anchor=False,
                )

            main_container.empty()
            st.query_params["gallery"] = selection

            with main_container.container():
                gallery[selection]()

    # --------------------------------------------
    # Embeded version
    # --------------------------------------------
    else:
        main_container = st.empty()

        with main_container.container():
            plotter = stpv.intro()
            stpyvista(
                plotter,
                panel_kwargs=dict(
                    orientation_widget=True,
                    interactive_orientation_widget=True,
                ),
            )

            st.subheader(
                "[🧊 `stpyvista`](https://stpyvista.streamlit.app)",
                anchor=False,
            )

            st.subheader(
                ":green[Show PyVista 3D visualizations in Streamlit]",
                anchor=False,
            )

            st.subheader(
                "[![Explore the gallery!](https://img.shields.io/badge/Community%20Cloud-Explore%20the%20gallery!-informational?style=flat&logo=streamlit&logoColor=red&color=pink)](https://stpyvista.streamlit.app)",
                anchor="Launch",
            )

            fill_install_instructions()
            fill_up_main_window()


if __name__ == "__main__":
    main()
