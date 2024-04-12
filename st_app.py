import streamlit as st
import pyvista as pv
import numpy as np
from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded  # , start_xvfb

import tempfile
from datetime import datetime
import inspect
# from collections import OrderedDict

## Debugging
from os import system

# Start app
import pantry.stpyvista_pantry as stpv

# Initial configuration
pv.start_xvfb()
st.session_state.is_app_embedded = st.session_state.get(
    "is_app_embedded", is_the_app_embedded()
)

if "FIRST_ACCESS" not in st.session_state:
    print(datetime.utcnow(), " Connected from <-- ??")
    st.session_state.FIRST_ACCESS = True

GALLERY = {
    "key": "🔑 Pass a key",
    "sphere": "✨ Textures and spheres",
    "stl": "📤 Upload a STL file",
    "align": "📐 Horizontal alignment",
    "grid": "🧱 Structured grid",
    "slider": "🔮 Sphere slider",
    "texture": "🐕 Image as texture",
    "xyz": "🌈 Colorbar and xyz",
    "opacity": "🗼 Opacity",
    "axes": "🪓 Axes and tickers",
    "solids": "🩴 Platonic solids",
    # "geovista": "🌎 Cartographic rendering",
    # "control": "🎛️ Control panel",
}


def fill_up_main_window():
    with st.expander("🛠️ Installation", expanded=True):
        """
        ```sh
        pip install stpyvista
        ```
        """

    with st.expander("🎮 Controls", expanded=True):
        controls_table = {
            "Control": [
                "LMB + Drag",
                "Ctrl + LMB + Drag",
                "Shift + Drag",
                "Scroll",
            ],
            "Description": [
                "Free rotate",
                "Rotate around center",
                "Pan",
                "Zoom",
            ],
        }
        st.dataframe(controls_table, use_container_width=True)

    with st.expander("✨ Code example", expanded=True):
        stpyvista(stpv.basic_example(), bokeh_resources="CDN")

        code, line_no = inspect.getsourcelines(stpv.basic_example)

        st.code(
            stpv.basic_import_text
            + "\n".join([line[4:-1] for line in code[2:-1]])
            + "\n## Pass a plotter to stpyvista"
            + "\nstpyvista(plotter)",
            language="python",
            line_numbers=True,
        )

    with st.expander("🔡 Also check:"):
        """
        * The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
        * Holoviz Panel VTK at [https://panel.holoviz.org/](https://panel.holoviz.org/reference/panes/VTK.html)
        * @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component
        * [Post](https://discuss.streamlit.io/t/stpyvista-show-pyvista-3d-visualizations-in-streamlit/31802) on streamlit discuss forum.

        """


def main():
    st.set_page_config(
        page_title="stpyvista",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # Add styling with CSS selectors
    with open("assets/style.css") as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

    if st.session_state.is_app_embedded:
        with open("assets/style_embed.css") as f:
            st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

    # --------------------------------------------
    # Full version
    # --------------------------------------------
    if not st.session_state.is_app_embedded:
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

        if selection_from_query in GALLERY.keys():
            st.session_state["gallery_select"] = selection_from_query

        with side_gallery_container:
            st.subheader("Gallery", anchor=False)

            selection = st.selectbox(
                "Gallery selection",
                GALLERY.keys(),
                index=None,
                label_visibility="collapsed",
                format_func=lambda x: GALLERY.get(x),
                placeholder="Select an option...",
                on_change=st.query_params.clear,
                key="gallery_select",
            )

            selection = selection_from_query or selection

        with side_other_container.container():
            # Add badges to sidebar
            with st.popover("📎"):
                with open("assets/badges.md") as f:
                    st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

        if not selection:
            with side_title_container.container():
                st.title("🧊", anchor=False)
                st.caption(
                    """
                    [`stpyvista`](https://github.com/edsaac/stpyvista) displays PyVista 
                    plotter objects in streamlit web apps using 
                    [`panel`](https://panel.holoviz.org/reference/panes/VTK.html)
                    """
                )

            with main_container.container():
                st.header("`stpyvista`", anchor="stpyvista")
                st.subheader(
                    "Show PyVista 3D visualizations in Streamlit", anchor=False
                )

                ## Send plotter to streamlit
                plotter = stpv.intro()
                stpyvista(
                    plotter,
                    panel_kwargs=dict(
                        orientation_widget=True, interactive_orientation_widget=True
                    ),
                )

                st.info("Check the examples gallery in the sidebar!", icon="👈")

                fill_up_main_window()

        # *************************************

        else:
            with side_title_container.container():
                st.header("🧊 `stpyvista`", anchor=False)

            if selection == "key":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🔑   Pass a key", divider="rainbow")

                    plotter = stpv.key()

                    cols = st.columns(2)

                    with cols[0]:
                        "### 🔑 With a key"
                        ## Pass a key to the component to avoid remounting it at each Streamlit rerun
                        with st.echo(code_location="below"):
                            stpyvista(plotter, key="pv_cube")

                    with cols[1]:
                        "### ⭕ Without a key"
                        ## Without a key, Streamlit re mounts the whole thing at each interaction :(
                        with st.echo(code_location="below"):
                            stpyvista(plotter)

                    st.button(
                        "🤔 Will this button make `stpyvista` to lose its state?",
                        use_container_width=True,
                    )

            elif selection == "sphere":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    "## ✨   Textures and spheres"
                    "### Specular and specular power"
                    stpyvista(stpv.spheres())
                    
                    "****"
                    "### Physically based rendering (PBR)"
                    stpyvista(stpv.pbr_test())

                    st.sidebar.caption("Check the [PyVista docs!](https://docs.pyvista.org/examples/02-plot/pbr.html)")
            
            elif selection == "stl":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():

                    def delmodel():
                        del st.session_state.fileuploader

                    ## Streamlit layout
                    st.header("📤   Upload a STL file", divider="rainbow")

                    placeholder = st.empty()
                    "&nbsp;"

                    with st.expander("I don't have an STL file"):
                        small_columns = st.columns(2)

                        with small_columns[1]:
                            st.download_button(
                                "🐇 [5.4M]",
                                stpv.stl_get("bunny"),
                                "bunny.stl",
                                help="Download an STL model of the Stanford bunny",
                                use_container_width=True,
                            )

                        with small_columns[0]:
                            st.download_button(
                                "🗼 [34M]",
                                stpv.stl_get("tower"),
                                "tower.stl",
                                help="Download an STL model of the Eiffel Tower",
                                use_container_width=True,
                            )

                    with placeholder:
                        uploadedFile = st.file_uploader(
                            "Upload a STL file:",
                            ["stl"],
                            accept_multiple_files=False,
                            key="fileuploader",
                        )

                    if uploadedFile:
                        ## Initialize pyvista reader and plotter
                        plotter = pv.Plotter(border=False, window_size=[500, 400])
                        plotter.background_color = "#f0f8ff"

                        ## Create a tempfile to keep the uploaded file as pyvista's API
                        ## only supports file paths but not buffers
                        with tempfile.NamedTemporaryFile(suffix="_streamlit") as f:
                            f.write(uploadedFile.getbuffer())
                            reader = pv.STLReader(f.name)

                            ## Read data and send to plotter
                            mesh = reader.read()
                            plotter.add_mesh(mesh, color="orange", specular=0.5)
                            plotter.view_xz()

                        ## Show in webpage
                        with placeholder.container():
                            st.button("🔙 Restart", "btn_rerender", on_click=delmodel)
                            stpyvista(plotter)

            elif selection == "align":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("📐   Horizontal alignment", divider="rainbow")

                    alignment = st.select_slider(
                        "Align",
                        ["left", "center", "right"],
                        label_visibility="collapsed",
                    )
                    sphere = stpv.sphere()

                    with st.echo(code_location="below"):
                        stpyvista(
                            sphere,
                            horizontal_align=alignment,
                            use_container_width=False,
                        )

            elif selection == "grid":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    "## 🧱 Structured grid"
                    code, line_no = inspect.getsourcelines(stpv.structuredgrid)
                    stpyvista(stpv.structuredgrid())

                    st.code(
                        "import numpy as np\n"
                        + stpv.basic_import_text
                        + "".join(code)
                        + """\nstpyvista(stpv_structuredgrid())""",
                        language="python",
                        line_numbers=True,
                    )

            elif selection == "slider":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("# 🔮   Sphere", divider="rainbow")

                    code = (
                        'res = st.slider("Resolution", 5, 100, 20, 5)\n\n'
                        "# Set up plotter\n"
                        "plotter = pv.Plotter(window_size=[300, 300])\n\n"
                        "# Create element\n"
                        "sphere = pv.Sphere(phi_resolution=res, theta_resolution=res)\n"
                        'plotter.add_mesh(sphere, name="sphere", show_edges=True)\n'
                        "plotter.view_isometric()\n\n"
                        "# Pass the plotter (not the mesh) to stpyvista\n"
                        "stpyvista(plotter)"
                    )

                    exec(code)
                    st.code(
                        stpv.basic_import_text + code,
                        language="python",
                        line_numbers=True,
                    )

            elif selection == "xyz":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🌈   Colorbar and orientation widget", divider="rainbow")

                    st.toast(
                        "Colorbar bug was fixed in [panel 1.3.2](https://github.com/holoviz/panel/releases/tag/v1.3.2).",
                        icon="🎇",
                    )

                    cube = stpv.cube()

                    "### 🌈 The three dots expand the colorbar legend"
                    with st.echo():
                        stpyvista(cube)

                    "****"
                    "### 🧭 Orientation widget: xyz directions"
                    with st.echo():
                        stpyvista(cube, panel_kwargs=dict(orientation_widget=True))

                    "****"
                    "### 🖱️ Make the orientation widget interactive "
                    with st.echo():
                        stpyvista(
                            cube,
                            panel_kwargs=dict(
                                orientation_widget=True,
                                interactive_orientation_widget=True,
                            ),
                        )

                    with st.sidebar:
                        "****"
                        st.info(
                            """Check the 
                            [`panel`](https://panel.holoviz.org/reference/panes/VTK.html) 
                            documentation for other `panel_kwargs` that could be 
                            passed to `stpyvista`. """
                        )

            elif selection == "opacity":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🏯   Opacity", divider="rainbow")

                    st.subheader("🔅 Single opacity value per mesh", anchor=False)
                    cols = st.columns([2, 1])

                    with cols[0]:
                        code_placeholder = st.empty()

                    with cols[1]:
                        "&nbsp;"
                        N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)
                        render_placeholder = st.empty()

                    with code_placeholder:
                        code, line_no = inspect.getsourcelines(stpv.tower)
                        st.code(
                            "import numpy as np\n"
                            "import matplotlib as mpl\n"
                            + stpv.basic_import_text
                            + "".join(code)
                            + "\n"
                            'N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)'
                            "tower = stpv_tower(N_BOXES)\n"
                            + "stpyvista(tower, panel_kwargs=dict(orientation_widget=True))",
                            line_numbers=True,
                        )

                    with render_placeholder:
                        tower = stpv.tower(N_BOXES)
                        stpyvista(tower, panel_kwargs=dict(orientation_widget=True))

                    ###########
                    "**********"
                    st.subheader("🔅 Opacity from a field", anchor=False)

                    COLOR_PICK = st.color_picker(
                        "`COLOR_PICK`",
                        value="#800080",
                        help="Pick a color for the plane",
                    )
                    render_placeholder = st.empty()
                    code_placeholder = st.empty()
                    "&nbsp;"

                    with code_placeholder:
                        code, line_no = inspect.getsourcelines(stpv.ripple)
                        st.code(
                            "import numpy as np\n"
                            + stpv.basic_import_text
                            + "".join(code)
                            + "\n"
                            'COLOR_PICK = st.color_picker("`COLOR_PICK`", value="#800080", help="Pick a color for the plane")\n'
                            "ripple = stpv_ripple()\n"
                            "ripple.actors['plane'].prop.color = COLOR_PICK\n"
                            "stpyvista(ripple, panel_kwargs=dict(orientation_widget=True))",
                            line_numbers=True,
                        )

                    with render_placeholder:
                        ripple = stpv.ripple()
                        ripple.actors["plane"].prop.color = COLOR_PICK
                        stpyvista(ripple, panel_kwargs=dict(orientation_widget=True))

            elif selection == "axes":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🪓   Axes", divider="rainbow")

                    with st.sidebar:
                        "***"
                        st.info(
                            "Check [`panel.pane.vtk`](https://panel.holoviz.org/api/panel.pane.vtk.html) for more options."
                        )

                    "### Axes configuration using `panel.pane.vtk`"

                    with st.expander("🪓 **Documentation**"):
                        st.write(
                            """
                            `axes` is a dictionary containing the parameters of the axes to
                            construct in the 3d view. It **must contain** at least `xticker`,
                            `yticker` and `zticker`.

                            A *ticker* is a dictionary which contains:
                            - `ticks : List[float] - required`.
                                > Positions in the scene coordinates of the corresponding
                                > axis' ticks.
                            - `labels : List[str] - optional`.
                                > Label displayed respectively to the `ticks` positions.
                                > If `labels` are not defined, they are inferred from the
                                > `ticks` array.

                            Other optional parameters for `axes` are:
                            - `digits : int`
                                > number of decimal digits when `ticks` are converted to `labels`.
                            - `fontsize : int`
                                > size in pts of the ticks labels.
                            - `show_grid : bool = True`
                                > If true the axes grid is visible.
                            - `grid_opacity : float` between 0-1.
                                > Defines the grid opacity.
                            - `axes_opacity : float` between 0-1.
                                > Defines the axes lines opacity.

                            """
                        )
                        st.caption(
                            "Source: [panel.holoviz.org](https://panel.holoviz.org/api/panel.pane.vtk.html#panel.pane.vtk.vtk.AbstractVTK)"
                        )

                    plotter = stpv.axis()
                    with st.echo("below"):
                        # Define axes to put in the rendered view
                        axes = dict(
                            ## tickers are required, it needs one for each axis
                            xticker=dict(
                                ticks=[0, 1, 2, 3, 4],  ## ticks are required
                                labels=["", "😎", "DOS", "🌺", "IV"],
                            ),
                            yticker=dict(
                                ticks=[0, 1, 2, 3, 4],  ## np.array fails
                                labels=[*" αβγδ"],  ## labels are optional
                            ),
                            zticker=dict(ticks=np.arange(0, 5, 1).tolist()),
                            ## Optional parameters
                            origin=[0, 0, 0],
                            fontsize=22,
                            show_grid=True,
                            grid_opacity=0.1,
                            axes_opacity=1.0,
                            digits=1,
                        )

                        # Pass those axes to panel_kwargs of stpyvista
                        stpyvista(
                            plotter,
                            panel_kwargs=dict(axes=axes, orientation_widget=True),
                        )

            elif selection == "geovista":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header(
                        "🌎 Running `geovista` for cartographic rendering",
                        divider="rainbow",
                    )
                    "&nbsp;"

                    planet = stpv.planet()

                    stpyvista(
                        planet,
                        panel_kwargs=dict(
                            orientation_widget=True, interactive_orientation_widget=True
                        ),
                    )

            elif selection == "texture":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🐕   Dog Elevation Model", divider="rainbow")
            
                    st.components.v1.iframe(
                        # "http://localhost:8501/?embed=True",
                        "https://stpyvista-dog-dem.streamlit.app/?embed=True",
                        scrolling=True,
                        height=470,
                    )
                
                with side_other_container:
                    st.subheader(
                        "🏞️ Explore the full version of this example at "
                        "[![Explore the app!](https://img.shields.io/badge/%20-Community%20Cloud-informational?style=flat&logo=streamlit&logoColor=red&color=pink)](https://stpyvista-dog-dem.streamlit.app)",
                        anchor=False
                    )

            elif selection == "control":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    pwd = st.text_input("Access code:", type="password")

                    if pwd == st.secrets.control.pwd:
                        if st.button("Clear cache"):
                            st.cache_resource.clear()

                        "********"

                        "Useful `ps` commands:"
                        """
                        - `ps -p <pid> -o %cpu,%mem,cmd`
                        - `ps aux --sort=-%mem`
                        """
                        """echo "* * * * * echo HELLO >> /mount/src/stpyvista-tests/my_log" >> my_cron; crontab my_cron"""

                        engine = st.selectbox("With:", ["os", "subprocess"], index=1)
                        code = st.text_input("Code", "ps aux --sort=-%mem")
                        output = ""

                        if code:
                            "Output"
                            if engine == "subprocess":
                                try:
                                    bash_code = f"output = subprocess.run({code.split()}, capture_output=True)"
                                    exec(bash_code)
                                    st.code(
                                        output.stdout.decode("utf-8"), language=None
                                    )
                                    st.code(
                                        output.stderr.decode("utf-8"), language=None
                                    )
                                except NameError:
                                    pass
                            elif engine == "os":
                                system(code)

            elif selection == "solids":
                main_container.empty()
                st.query_params["gallery"] = selection

                with main_container.container():
                    st.header("🩴   Platonic solids", divider="rainbow")
                    "&nbsp;"

                    labels = ["▲", "■", "◭", "⬟", "◑"]
                    cols = st.columns(5)

                    for col, name, solid, label in zip(
                        cols, stpv.SOLIDS, stpv.solids(), labels
                    ):
                        with col:
                            with st.popover(label, use_container_width=True):
                                f"### **{name.title()}**"
                                stpyvista(solid)

                    st.caption(
                        "Solids from [PyVista](https://docs.pyvista.org/version/stable/api/utilities/geometric.html)"
                    )

    # --------------------------------------------
    # Embeded version
    # --------------------------------------------
    else:
        main_container = st.empty()

        with main_container.container():
            st.header("🧊 `stpyvista`")

            plotter = stpv.intro()

            stpyvista(
                plotter,
                panel_kwargs=dict(
                    orientation_widget=True, interactive_orientation_widget=True
                ),
            )

            st.subheader("Show PyVista 3D visualizations in Streamlit", anchor=False)
            st.subheader(
                "[![Explore the gallery!](https://img.shields.io/badge/Community%20Cloud-Explore%20the%20gallery!-informational?style=flat&logo=streamlit&logoColor=red&color=pink)](https://stpyvista.streamlit.app)",
                anchor="Launch",
            )

            fill_up_main_window()


if __name__ == "__main__":
    main()
