import numpy as np
import pyvista as pv
from itertools import product
from random import random
import streamlit as st
import matplotlib as mpl
import geovista as gv
from collections import namedtuple
from io import BytesIO
from typing import Literal
from pathlib import Path
from PIL import Image

basic_import_text = (
    "import streamlit as st\n"
    "import pyvista as pv\n"
    "from stpyvista import stpyvista\n\n"
)


## Pyvista code
@st.cache_resource
def intro(dummy: str = "robot"):
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
def basic_example(dummy: str = "sphere") -> pv.Plotter:
    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400, 400])

    ## Create a mesh
    mesh = pv.Sphere(radius=1.0, center=(0, 0, 0))

    ## Associate a scalar field to the mesh
    x, y, z = mesh.cell_centers().points.T
    mesh["My scalar"] = z

    ## Add mesh to the plotter
    plotter.add_mesh(
        mesh,
        scalars="My scalar",
        cmap="prism",
        show_edges=True,
        edge_color="#001100",
        ambient=0.2,
    )

    ## Some final touches
    plotter.background_color = "white"
    plotter.view_isometric()

    return plotter


## Initialize a plotter object
@st.cache_resource
def key(dummy: str = "key"):
    plotter = pv.Plotter(window_size=[250, 250])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(mesh, scalars="myscalar", cmap="bwr", line_width=1)
    plotter.view_isometric()
    return plotter


## Cube
@st.cache_resource
def cube(dummy: str = "cube"):
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.Cube(center=(0, 0, 0))
    mesh["myscalar"] = mesh.points[:, 2] * mesh.points[:, 0]
    plotter.add_mesh(
        mesh, scalars="myscalar", cmap="bwr", line_width=2, show_edges=True
    )
    plotter.background_color = "white"
    plotter.view_isometric()
    plotter.add_title("◱ Check the corners ◲", color="purple", font_size=20)
    return plotter


## Many spheres
@st.cache_resource
def spheres(dummy: str = "spheres"):
    specular_values = [0.0, 0.25, 0.50, 0.75, 1.0]
    power_values = [64, 32, 16, 8]
    sphere_kwargs = dict(radius=0.51, phi_resolution=50, theta_resolution=50)
    plotter = pv.Plotter(border=False, window_size=[600, 400])
    plotter.background_color = "white"

    # Add a bunch of spheres with different properties
    for j, specular in enumerate(specular_values):
        for i, power in enumerate(power_values):
            sphere = pv.Sphere(center=(0, i, j), **sphere_kwargs)
            plotter.add_mesh(
                sphere,
                color="purple",
                lighting=True,
                specular=specular,
                specular_power=power,
                ambient=0.30,
            )

    plotter.add_floor("-y", lighting=True, color="pink", pad=0.10)
    plotter.view_vector((-1, 0, 0), (0, 1, 0))

    return plotter


@st.cache_resource
def pbr_test(dummy: str = "pbr"):
    
    plotter = pv.Plotter(
        border=False, 
        window_size=[600, 400], 
        shape=[1, 2],
    )
    plotter.background_color = "grey"

    spheres = [
        pv.Sphere(),
        pv.Sphere(radius=0.25, center=(0.5, 0, 0.5))
    ]

    colors = ['silver', '#003366']

    light_kwargs = dict(
        specular=0.50,
        specular_power=16,
        ambient=0.10,
    )

    # Add a bunch of spheres with different properties
    plotter.subplot(0, 0)    
    for sphere, color in zip(spheres, colors):
        plotter.add_mesh(
            sphere,
            color=color,
            **light_kwargs
        )
    plotter.add_text("PBR off")
    plotter.view_isometric()

    plotter.subplot(0, 1)    
    for sphere, color in zip(spheres, colors):
        plotter.add_mesh(
            sphere,
            color=color,
            pbr=True,
            metallic=0.75,
            **light_kwargs
        )
    plotter.add_text("PBR on")

    plotter.view_isometric()
    plotter.link_views()

    return plotter


@st.cache_resource
def tower(n_boxes: int):
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


@st.cache_resource
def sphere(dummy: str = "sphere"):
    # Single sphere
    pl = pv.Plotter(window_size=[300, 200])
    pl.set_background("#D3EEFF")
    pl.add_mesh(pv.Sphere(center=(1, 0, 1)))
    pl.view_isometric()
    return pl


## Add boxes to pyvista plotter
@st.cache_resource
def axis(dummy: str = "axis"):
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
def structuredgrid(dummy: str = "grid"):
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
def ripple(dummy: str = "ripple"):
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
def planet(dummy: str = "planet"):
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


@st.cache_resource
def stl_get(which: Literal["bunny", "tower"] = "bunny"):
    stl_path = Path(f"assets/stl/{which}.stl")

    if stl_path.exists():
        with BytesIO() as buffer, open(stl_path, "rb") as f:
            buffer.write(f.read())
            data = buffer.getvalue()

        return data


@st.cache_resource
def dog_texture(dummy: str = "dog"):
    PATH_TO_JPG = "./assets/img/gloria_pickle.jpg"
    tex = pv.read_texture(PATH_TO_JPG)

    with Image.open(PATH_TO_JPG) as im:
        gray_scale = im.convert(mode="L").resize([x // 2 for x in im.size])
        width, height = gray_scale.size

    # Create mesh grid
    x = np.arange(width)
    y = np.arange(height, 0, -1)
    xx, yy = np.meshgrid(x, y)
    z = -0.25 * (np.array(gray_scale))

    # Generate surface
    surface = (
        pv.StructuredGrid(xx, yy, z)
        .triangulate()
        .extract_surface()
        .smooth()
        .texture_map_to_plane(use_bounds=True, inplace=True)
    )

    # Lower elevations -> transparent
    zp = surface.points[:, 2]
    opacity = np.interp(zp, [zp.min(), 0.90 * zp.max()], [0, 1])

    # Assemble plotter
    plotter = pv.Plotter()
    plotter.window_size = [400, 350]
    plotter.background_color = "#efe4cf"

    plotter.add_mesh(
        surface,
        texture=tex,
        show_scalar_bar=False,
        opacity=opacity,
        name="dog",
    )

    # Zooming and camera configs
    plotter.camera_position = "xy"
    plotter.camera.elevation = -10
    pos = plotter.camera.position
    fcp = plotter.camera.focal_point
    plotter.camera.position = [0.65 * p + 0.35 * f for p, f in zip(pos, fcp)]

    # Last touches
    plotter.add_text(
        "🐾",
        position="upper_left",
        color="black",
        font_size=18,
        shadow=True,
    )

    return plotter


PLATONIC_SOLIDS = [
    "tetrahedron",
    "cube",
    "octahedron",
    "dodecahedron",
    "icosahedron",
]

SOLIDS = PLATONIC_SOLIDS


@st.cache_resource
def solids(dummy: "str" = "platonic") -> list[pv.Plotter]:
    plotters = []

    for kind in PLATONIC_SOLIDS:
        solid = pv.PlatonicSolid(kind, radius=0.5)
        plotter = pv.Plotter()
        plotter.window_size = [300, 300]
        plotter.background_color = "#e1743b"
        plotter.add_mesh(
            solid,
            show_scalar_bar=False,
            edge_color="w",
            color="#9d0f0e",
            show_edges=True,
        )
        plotter.view_isometric()
        plotters.append(plotter)

    return plotters


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
