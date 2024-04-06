import streamlit as st
from pyvista.plotting.utilities import start_xvfb
from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded

# Start app
from stpyvista_pantry import dog_texture

# Initial configuration
start_xvfb()
st.session_state.is_app_embedded = st.session_state.get(
    "is_app_embedded", is_the_app_embedded()
)


def main():
    st.set_page_config(
        page_title="stpyvista: Dog Canyon",
        page_icon="🐕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Add some styling with CSS selectors
    for style_sheet in ["./assets/style.css", "./assets/style_embed.css"]:
        with open(style_sheet) as f:
            st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
    
    # Load pyvista Plotter`
    dog = dog_texture()

    if not st.session_state.is_app_embedded:
        st.markdown(
            """
            <style>
                p{
                    text-align: center; 
                    line-height: 1em;
                }
                div[data-testid="stImage"] img{
                    border: 7px ridge rgba(211, 220, 50, .6);
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    width: max(25%, 12vw);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.header("🐕   Dog Elevation Model (DEM)", divider="rainbow")
        "&nbsp;"

        cols = st.columns([1, 3])

        with cols[0]:
            "Generate a digital elevation model from an image's brightness."
            st.image("./assets/img/gloria_pickle.jpg")
            st.caption(
                "Gloria from [The Coding Train](https://thecodingtrain.com/challenges/181-image-stippling)"
            )

        with cols[1]:
            container_3d = st.container()

    else:
        container_3d = st.container()

    with container_3d:
        stpyvista(
            dog,
            panel_kwargs=dict(
                orientation_widget=True, interactive_orientation_widget=True
            ),
            use_container_width=True,
        )

    if st.session_state.is_app_embedded:
        st.markdown(
            """
            <style>
                body{
                    background-color: rgba(0,0,0,0);
                }
                div[data-testid="stAppViewBlockContainer"]{
                    padding: 0; 
                }
                iframe[title="stpyvista.rendered"]{
                    display: block; 
                    width: 95vw; 
                    border: none;
                }

                div[data-testid="stVerticalBlockBorderWrapper"]{
                    transform: translateY(-12px);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
