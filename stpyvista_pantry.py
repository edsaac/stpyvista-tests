import numpy as np
import pyvista as pv
from itertools import product
from random import random
import streamlit as st
import matplotlib as mpl
import geovista as gv
from collections import namedtuple

basic_import_text = (
    "import streamlit as st\n"
    "import pyvista as pv\n"
    "from stpyvista import stpyvista\n\n"
)


## Pyvista code
@st.cache_resource
def stpv_intro(dummy: str = "robot"):
    plotter = pv.Plotter()

    head = pv.Cylinder(radius=3.5, height=8)
    nose = pv.Cylinder(radius=0.5, height=8, direction=(0, 0, 1), center=(0, 0, 1.7))
    eye_left = pv.Cylinder(
        radius=1.0, height=4, direction=(0, 0, 1), center=(-2.0, 1, 2)
    )
    eye_left_p = pv.Cylinder(
        radius=0.3, height=4.1, direction=(0, 0, 1), center=(-2.0, 1, 2)
    )
    eye_right = pv.Cylinder(
        radius=1.0, height=4, direction=(0, 0, 1), center=(2.0, 1, 2)
    )
    eye_right_p = pv.Cylinder(
        radius=0.3, height=4.1, direction=(0, 0, 1), center=(2.0, 1, 2)
    )

    plotter.add_mesh(head, color="grey")
    plotter.add_mesh(nose, color="red")
    plotter.add_mesh(eye_left, color="white")
    plotter.add_mesh(eye_right, color="white")
    plotter.add_mesh(eye_left_p, color="green")
    plotter.add_mesh(eye_right_p, color="green")

    plane = pv.Plane(center=[0, -3.65, 0], direction=[0, 1, 0], i_size=12, j_size=12)
    plotter.add_mesh(plane, color="#09ab3b", show_edges=True)

    plotter.background_color = "white"
    plotter.view_xy()
    plotter.camera.azimuth = 25
    plotter.camera.elevation = 15

    plotter.window_size = [450, 300]
    return plotter


## Usage example
@st.cache_resource
def stpv_usage_example(dummy: str = "cube") -> pv.Plotter:
    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400, 400])

    ## Create a mesh with a cube
    mesh = pv.Cube(center=(0, 0, 0))

    ## Add some scalar field associated to the mesh
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 1] * mesh.points[:, 0]

    ## Add mesh to the plotter
    plotter.add_mesh(
        mesh, scalars="myscalar", cmap="bwr", show_edges=True, edge_color="#001100"
    )

    ## Final touches
    plotter.background_color = "white"
    plotter.view_isometric()

    return plotter


## Initialize a plotter object
@st.cache_resource
def stpv_key(dummy: str = "key"):
    plotter = pv.Plotter(window_size=[250, 250])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
    plotter.view_isometric()
    return plotter


## Cube
@st.cache_resource
def stpv_cube(dummy: str = "cube"):
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
    plotter.background_color = "white"
    plotter.view_isometric()
    plotter.add_title("◱ Check the corners ◲", color="purple", font_size=20)
    return plotter


## Many spheres
@st.cache_resource
def stpv_spheres(dummy: str = "spheres"):
    colors = ["red", "teal", "black", "orange", "silver"]
    plotter = pv.Plotter(border=False, window_size=[600, 400])
    plotter.background_color = "white"

    # Add a bunch of spheres with different properties
    for i in range(5):
        for j in range(6):
            sphere = pv.Sphere(radius=0.5, center=(0.0, 4 - i, j))
            plotter.add_mesh(
                sphere, color=colors[i], pbr=True, metallic=i / 4, roughness=j / 5
            )

    plotter.view_vector((-1, 0, 0), (0, 1, 0))
    plotter.camera.zoom(1.5)
    return plotter


## Add boxes to pyvista plotter
@st.cache_resource
def stpv_tower(n_boxes: int):
    ## Sample a matplotlib colormap
    cmap = mpl.cm.tab20c_r
    colors = cmap(np.linspace(0, 1, n_boxes))

    ## Initialize plotter
    plotter = pv.Plotter()
    for i, c in enumerate(colors, start=1):
        cube = pv.Cube(center=(0, 0, i), x_length=2.5, y_length=1.5, z_length=0.75)
        cube = cube.rotate_z(i * 90 / 15, point=(0, 0, 0), inplace=True)
        plotter.add_mesh(
            cube, edge_color="black", color=c, opacity=i / n_boxes, show_edges=True
        )

    ## Plotter configuration
    plotter.background_color = "#ffffff"
    plotter.camera.zoom("tight")
    plotter.view_isometric()
    plotter.window_size = [200, 500]
    return plotter


# Single sphere
@st.cache_resource
def stpv_sphere(dummy: str = "sphere"):
    pl = pv.Plotter(window_size=[300, 200])
    pl.set_background("#D3EEFF")
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    pl.view_isometric()
    return pl


## Add boxes to pyvista plotter
@st.cache_resource
def stpv_axis(dummy: str = "axis"):
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


# Set up plotter
@st.cache_resource
def stpv_structuredgrid(dummy: str = "grid"):
    # Create coordinate data
    x = np.arange(-10, 10, 0.5)
    y = np.arange(-10, 10, 0.5)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))

    plotter = pv.Plotter()
    surface = pv.StructuredGrid(x, y, z)
    plotter.add_mesh(surface, color="pink", show_edges=True, edge_color="k")
    plotter.background_color = "white"
    plotter.view_isometric()
    plotter.window_size = [600, 400]
    return plotter


## Ripple
@st.cache_resource
def stpv_ripple(dummy: str = "ripple"):
    # Create coordinate data
    x, y = np.arange(-10, 10, 0.25), np.arange(-10, 10, 0.25)
    x, y = np.meshgrid(x, y)
    z = 4 * np.sin(np.sqrt(x**2 + y**2))

    # Initialize plotter
    plotter = pv.Plotter()
    plane = pv.Plane(center=[0, 0, -5.2], direction=[0, 0, 1], i_size=25, j_size=25)
    plane.point_data.clear()
    plotter.add_mesh(
        plane, color="#00FF7F", show_edges=True, edge_color="purple", name="plane"
    )

    # Add the surface
    surface = pv.StructuredGrid(x, y, z)
    zp = surface.points[:, 2]
    surface["opacity"] = np.interp(zp, [zp.min(), zp.max()], [0.2, 1])
    plotter.add_mesh(
        surface,
        color="#ff0000",
        opacity=surface["opacity"],
        show_scalar_bar=False,
        name="ripple",
    )

    ## Final touches
    plotter.camera.zoom("tight")
    plotter.view_isometric()
    plotter.window_size = [400, 400]
    return plotter


## Geovista
@st.cache_resource
def stpv_planet(dummy: str = "planet"):
    Point = namedtuple("Point", ["lat", "lon"])

    x = np.arange(-180, 184, 4)  # Lon
    y = np.arange(90, -94, -4)  # Lat
    xx, yy = np.meshgrid(np.deg2rad(x), np.deg2rad(y))

    p = Point(np.deg2rad(4.60971), np.deg2rad(-74.08175))  # Bogotá
    radius = 6_371  # Radius Earth

    # "d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)])"
    # data = np.abs(yy)
    data = (
        2
        * radius
        * np.arcsin(
            np.sin((yy - p.lat) / 2) ** 2
            + np.cos(p.lat) * np.cos(yy) * np.sin((xx - p.lon) / 2) ** 2
        )
    )

    blob = gv.Transform.from_1d(x, y, data=data, name="Distance to Bogota [km]")

    plotter = gv.GeoPlotter()
    plotter.window_size = [450, 450]
    plotter.background_color = "#080D35"
    plotter.add_graticule(
        lon_step=10,
        lat_step=10,
        mesh_args=dict(
            color="pink",
            opacity=0.2,
        ),
    )
    plotter.add_coastlines(
        color="white",
        line_width=12,
        resolution="110m",
    )
    plotter.view_xz(negative=False)
    plotter.add_text(
        "🌎 Distance to Bogotá",
        position="upper_left",
        color="w",
        font_size=15,
        shadow=True,
    )

    plotter.add_text(
        "▛ geovista ▟",
        position="lower_edge",
        color="pink",
        font_size=12,
        shadow=True,
    )

    plotter.add_mesh(
        blob,
        show_edges=False,
        style="surface",
        cmap="CET_R1_r",
        clim=[0, 0.95 * np.pi * radius],
    )

    return plotter


if __name__ == "__main__":
    pass

# else:
#     stpv_intro()
#     stpv_key()
#     stpv_cube()
#     stpv_sphere()
#     stpv_spheres()
#     stpv_tower(8)
#     stpv_structuredgrid()
#     stpv_axis()
#     stpv_ripple()
#     stpv_planet()
