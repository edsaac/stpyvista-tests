import streamlit as st
from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded, start_xvfb

# Start app
from stpyvista_pantry import dog_texture

# Initial configuration
start_xvfb()
st.session_state.is_app_embedded = st.session_state.get("is_app_embedded", is_the_app_embedded())

def main():
    
    st.set_page_config(
        page_title="stpyvista: Dog Canyon",
        page_icon="🐕",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Add some styling with CSS selectors
    with open("./assets/style.css") as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

    with open("./assets/style_embed.css") as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
    
    dog = dog_texture()

    if not IS_APP_EMBED:
        st.header("🐕   Dog Elevation Model (DEM)", divider="rainbow")
        "&nbsp;"

        cols = st.columns([1,3])

        with cols[0]:
            st.markdown(
                """
                <p style="text-align: center;">
                Generate a digital elevation model from an image's brightness.
                </p>
                """,
                unsafe_allow_html=True
            )

            _, subcol, _ = st.columns([1, 3, 1])
            with subcol:
                st.image("./assets/img/gloria_pickle.jpg", use_column_width=True)
                st.caption(
                    "Gloria from [The Coding Train](https://thecodingtrain.com/challenges/181-image-stippling)"
                )

        with cols[1]:
            container_3d = st.container()

    if IS_APP_EMBED:
        container_3d = st.container()

    with container_3d:
        stpyvista(
            dog,
            panel_kwargs=dict(
                orientation_widget=True, interactive_orientation_widget=True
            ),
            use_container_width=True,
        )

if __name__ == "__main__":
    main()