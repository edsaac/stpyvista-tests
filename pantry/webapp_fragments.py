import streamlit as st
import pyvista as pv
import numpy as np
from stpyvista import stpyvista
import pantry.stpyvista_pantry as stpv

import tempfile
import inspect
from os import system


@st.experimental_fragment
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


@st.experimental_fragment
def option_key():
    """🔑 Pass a key"""

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


@st.experimental_fragment
def option_sphere():
    """✨ Textures and spheres"""

    headers_kwargs = dict(anchor=False)
    st.header("✨   Textures and spheres", **headers_kwargs)
    st.subheader("Specular and specular power", **headers_kwargs)

    stpyvista(stpv.spheres())

    "****"
    st.subheader("Physically based rendering (PBR)", **headers_kwargs)

    stpyvista(stpv.pbr_test())

    st.info(
        "Check the [PyVista docs!](https://docs.pyvista.org/examples/02-plot/pbr.html)",
        icon="📌",
    )


@st.experimental_fragment
def option_stl():
    """📤 Upload a STL file"""

    def delmodel():
        del st.session_state.fileuploader

    st.header("📤   Upload a STL file", anchor=False, divider="rainbow")

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


@st.experimental_fragment
def option_align():
    """📐 Horizontal alignment"""

    st.header("📐   Horizontal alignment", anchor=False)

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


@st.experimental_fragment
def option_grid():
    """🧱 Structured grid"""

    st.header("🧱 Structured grid", anchor=False, divider="rainbow")
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


@st.experimental_fragment
def option_slider():
    """🔮 Sphere slider"""

    st.header("# 🔮   Sphere", divider="rainbow", anchor=False)

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


@st.experimental_fragment
def option_texture():
    """🐕 Image as texture"""
    st.header("🐕   Dog Elevation Model", divider="rainbow")

    st.components.v1.iframe(
        # "http://localhost:8502/?embed=True",
        "https://stpyvista-dog-dem.streamlit.app/?embed=True",
        scrolling=True,
        height=390,
    )

    st.info(
        "🏞️ Explore the full version of this example at "
        "[![Explore the app!](https://img.shields.io/badge/%20-Community%20Cloud-informational?style=flat&logo=streamlit&logoColor=red&color=pink)](https://stpyvista-dog-dem.streamlit.app)",
        anchor=False,
    )



@st.experimental_fragment
def option_xyz():
    """🌈 Colorbar and xyz"""
    st.header("🌈   Colorbar and orientation widget", divider="rainbow", anchor=False)

    st.toast(
        "Colorbar bug was fixed in [panel>=1.3.2](https://github.com/holoviz/panel/releases/tag/v1.3.2).",
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


@st.experimental_fragment
def option_opacity():
    """🗼 Opacity"""

    st.header("🏯   Opacity", divider="rainbow", anchor=False)
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
            "import matplotlib as mpl\n" + stpv.basic_import_text + "".join(code) + "\n"
            'N_BOXES = st.number_input("`N_BOXES`", 0, 12, 8, 1)'
            "tower = stpv_tower(N_BOXES)\n"
            + "stpyvista(tower, panel_kwargs=dict(orientation_widget=True))",
            line_numbers=True,
        )

    with render_placeholder:
        tower = stpv.tower(N_BOXES)
        stpyvista(tower, panel_kwargs=dict(orientation_widget=True))

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
            "import numpy as np\n" + stpv.basic_import_text + "".join(code) + "\n"
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


@st.experimental_fragment
def option_axes():
    """🪓 Axes and tickers"""

    st.header("🪓   Axes", divider="rainbow", anchor=False)

    with st.sidebar:
        "***"
        st.info(
            "Check [`panel.pane.vtk`](https://panel.holoviz.org/api/panel.pane.vtk.html) for more options."
        )

    st.subheader("Axes configuration using `panel.pane.vtk`", anchor=False)

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


@st.experimental_fragment
def option_solids():
    """🩴 Platonic solids"""
    st.header("🩴   Platonic solids", divider="rainbow", anchor=False)

    "&nbsp;"

    labels = ["▲", "■", "◭", "⬟", "◑"]
    cols = st.columns(5)

    for col, name, solid, label in zip(cols, stpv.SOLIDS, stpv.solids(), labels):
        with col:
            with st.popover(label, use_container_width=True):
                f"### **{name.title()}**"
                stpyvista(solid)

    st.caption(
        "Solids from [PyVista](https://docs.pyvista.org/version/stable/api/utilities/geometric.html)"
    )


@st.experimental_fragment
def option_geovista():
    """🌎 Cartographic rendering"""
    st.header(
        "🌎 Running `geovista` for cartographic rendering",
        divider="rainbow",
        anchor=False,
    )
    "&nbsp;"

    planet = stpv.planet()

    stpyvista(
        planet,
        panel_kwargs=dict(orientation_widget=True, interactive_orientation_widget=True),
    )

    st.info(
        "Explore the [`geovista`](https://github.com/bjlittle/geovista) project.",
        icon='🌎',
    )



@st.experimental_fragment
def option_control():
    """🎛️ Control panel"""

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
                    bash_code = (
                        f"output = subprocess.run({code.split()}, capture_output=True)"
                    )
                    exec(bash_code)
                    st.code(output.stdout.decode("utf-8"), language=None)
                    st.code(output.stderr.decode("utf-8"), language=None)
                except NameError:
                    pass

            elif engine == "os":
                system(code)


gallery = {
    "key": option_key,
    "sphere": option_sphere,
    "stl": option_stl,
    "align": option_align,
    "grid": option_grid,
    "slider": option_slider,
    "texture": option_texture,
    "xyz": option_xyz,
    "opacity": option_opacity,
    "axes": option_axes,
    "solids": option_solids,
    "geovista": option_geovista,
    # "control": option_control,
}

if __name__ == "__main__":
    pass