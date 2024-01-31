import streamlit as st
from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded, start_xvfb

import tempfile
from datetime import datetime
import inspect

## Debugging
from os import system

# Initial configuration
if "IS_APP_EMBED" not in st.session_state:
    st.session_state.IS_APP_EMBED = is_the_app_embedded()
IS_APP_EMBED = st.session_state.IS_APP_EMBED

st.set_page_config(
    page_title="stpyvista",
    page_icon="🧊",
    layout="wide" if IS_APP_EMBED else "centered",
    initial_sidebar_state="collapsed",
)

if "FIRST_ACCESS" not in st.session_state:
    print(datetime.utcnow(), " Connected from <-- ??")
    st.session_state.FIRST_ACCESS = True


if "IS_XVFB_RUNNING" not in st.session_state:
    start_xvfb()
    st.session_state.IS_XVFB_RUNNING = True

# Add some styling with CSS selectors
with open("assets/style.css") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

# Add badges to sidebar
if not IS_APP_EMBED:
    with st.sidebar:
        with open("assets/badges.md") as f:
            st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

GALLERY = {
    "KEY": "🔑 Pass a key",
    # "SPHERE": "✨ Textures and spheres",
    # "STL":    "📤 Upload a STL file",
    "ALIGN": "📐 Horizontal alignment",
    "GRID": "🧱 Structured grid",
    # "SLIDER": "🔮 Sphere slider",
    "XYZ": "🌈 Colorbar and xyz",
    # "OPACITY": "🗼 Opacity",
    "AXES": "🪓 Axes and tickers",
    # "GEOVISTA": "🌎 Cartographic rendering",
    "CONTROL": "🎛️ Control panel",
}

# Start app
from stpyvista_pantry import *

main_container = st.empty()

with st.sidebar:
    st.title("🧊")
    st.header("`stpyvista`")
    "****"
    "### Gallery"
    selection = st.selectbox(
        "Gallery selection",
        GALLERY.keys(),
        index=None,
        label_visibility="collapsed",
        format_func=lambda x: GALLERY.get(x, "Select an option..."),
    )


if not selection:
    with main_container.container():
        st.title("🧊 `stpyvista`")
        st.subheader("Show PyVista 3D visualizations in Streamlit")

        ## Send plotter to streamlit
        plotter = stpv_intro()
        stpyvista(
            plotter,
            panel_kwargs=dict(
                orientation_widget=True, interactive_orientation_widget=True
            ),
        )

        with st.sidebar:
            "****"
            """
            `stpyvista` displays PyVista plotter objects in streamlit web apps,
            using [`panel`](https://panel.holoviz.org/reference/panes/VTK.html).
            """

        st.info("Check the gallery in the sidebar!", icon="👈")

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
                "Description": ["Free rotate", "Rotate around center", "Pan", "Zoom"],
            }
            st.dataframe(controls_table, use_container_width=True)

        with st.expander("✨ Code example"):
            code, line_no = inspect.getsourcelines(stpv_usage_example)

            st.code(
                basic_import_text + "".join(code) + "\n## Pass a plotter to stpyvista"
                """\nstpyvista(stpv_usage_example())""",
                language="python",
                line_numbers=True,
            )

            stpyvista(stpv_usage_example())

        with st.expander("🔡 Also check:"):
            """
            * The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
            * Holoviz Panel VTK at [https://panel.holoviz.org/](https://panel.holoviz.org/reference/panes/VTK.html)
            * @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component
            * [Post](https://discuss.streamlit.io/t/stpyvista-show-pyvista-3d-visualizations-in-streamlit/31802) on streamlit discuss forum.

            """

# *************************************

elif selection == "KEY":
    main_container.empty()
    with main_container.container():
        "## 🔑   Pass a key"

        plotter = stpv_key()

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

elif selection == "SPHERE":
    main_container.empty()
    with main_container.container():
        "## ✨   Textures and spheres"

        with st.sidebar:
            "***"
            st.error("Textures in `panel` are not rendered?")

        stpyvista(stpv_spheres())
        st.caption(
            "Code adapted from https://docs.pyvista.org/examples/02-plot/pbr.html"
        )

elif selection == "STL":
    main_container.empty()
    with main_container.container():

        def delmodel():
            del st.session_state.fileuploader

        ## Streamlit layout
        "## 📤   Upload a STL file"
        placeholder = st.empty()

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
                plotter.add_mesh(mesh, color="salmon")
                plotter.view_isometric()

            ## Show in webpage
            with placeholder.container():
                st.button("Restart", "btn_rerender", on_click=delmodel)
                stpyvista(plotter, key="my_stl")

elif selection == "ALIGN":
    main_container.empty()
    with main_container.container():
        "## 📐   Horizontal alignment"

        alignment = st.select_slider(
            "Align", ["left", "center", "right"], label_visibility="collapsed"
        )

        stpyvista(stpv_sphere(), horizontal_align=alignment, use_container_width=False)

elif selection == "GRID":
    main_container.empty()
    with main_container.container():
        "## 🧱 Structured grid"
        code, line_no = inspect.getsourcelines(stpv_structuredgrid)
        stpyvista(stpv_structuredgrid())

        st.code(
            "import numpy as np\n"
            + basic_import_text
            + "".join(code)
            + """\nstpyvista(stpv_structuredgrid())""",
            language="python",
            line_numbers=True,
        )

elif selection == "SLIDER":
    main_container.empty()
    with main_container.container():
        "## 🔮 Sphere"

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
        st.code(basic_import_text + code, language="python", line_numbers=True)

elif selection == "XYZ":
    main_container.empty()
    with main_container.container():
        "## 🌈 Colorbar and orientation widget"

        st.toast(
            "Colorbar bug was fixed in [panel 1.3.2](https://github.com/holoviz/panel/releases/tag/v1.3.2).",
            icon="🎇",
        )

        cube = stpv_cube()

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
                    orientation_widget=True, interactive_orientation_widget=True
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

elif selection == "OPACITY":
    main_container.empty()
    with main_container.container():
        "## 🏯 Opacity"
        "### 🔅 Single opacity value per mesh"
        cols = st.columns([2, 1])

        with cols[0]:
            code_placeholder = st.empty()

        with cols[1]:
            "&nbsp;"
            N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)
            render_placeholder = st.empty()

        with code_placeholder:
            code, line_no = inspect.getsourcelines(stpv_tower)
            st.code(
                "import numpy as np\n"
                "import matplotlib as mpl\n" + basic_import_text + "".join(code) + "\n"
                'N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)'
                "tower = stpv_tower(N_BOXES)\n"
                + "stpyvista(tower, panel_kwargs=dict(orientation_widget=True))",
                line_numbers=True,
            )

        with render_placeholder:
            tower = stpv_tower(N_BOXES)
            stpyvista(tower, panel_kwargs=dict(orientation_widget=True))

        ###########
        "**********"
        "### 🔅 Opacity from a field"
        COLOR_PICK = st.color_picker(
            "`COLOR_PICK`", value="#800080", help="Pick a color for the plane"
        )
        render_placeholder = st.empty()
        code_placeholder = st.empty()
        "&nbsp;"

        with code_placeholder:
            code, line_no = inspect.getsourcelines(stpv_ripple)
            st.code(
                "import numpy as np\n" + basic_import_text + "".join(code) + "\n"
                'COLOR_PICK = st.color_picker("`COLOR_PICK`", value="#800080", help="Pick a color for the plane")\n'
                "ripple = stpv_ripple()\n"
                "ripple.actors['plane'].prop.color = COLOR_PICK\n"
                "stpyvista(ripple, panel_kwargs=dict(orientation_widget=True))",
                line_numbers=True,
            )

        with render_placeholder:
            ripple = stpv_ripple()
            ripple.actors["plane"].prop.color = COLOR_PICK
            stpyvista(ripple, panel_kwargs=dict(orientation_widget=True))

elif selection == "AXES":
    main_container.empty()
    with main_container.container():
        "## 🪓 Axes"

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

        plotter = stpv_axis()
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
            stpyvista(plotter, panel_kwargs=dict(axes=axes, orientation_widget=True))

elif selection == "GEOVISTA":
    main_container.empty()
    with main_container.container():
        "## 🌎 Running `geovista` for cartographic rendering"

        planet = stpv_planet()

        stpyvista(
            planet,
            panel_kwargs=dict(
                orientation_widget=True, interactive_orientation_widget=True
            ),
        )

elif selection == "CONTROL":
    main_container.empty()
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
                        st.code(output.stdout.decode("utf-8"), language=None)
                        st.code(output.stderr.decode("utf-8"), language=None)
                    except NameError:
                        pass
                elif engine == "os":
                    system(code)
