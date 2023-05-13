# 🧊 `stpyvista`: Show PyVista 3D visualizations in Streamlit

<p align=center>🎈 <strong>Examples and tests repository</strong> 🎈</p>

<p align=center>
<a href="https://github.com/edsaac/stpyvista"><img alt="stpyvista source code" src="https://img.shields.io/static/v1?label=:&message=Source%20code&color=informational&logo=github"></a>
<a href="https://pypi.org/project/stpyvista/"><img alt="stpyvista pypi version" src="https://badgen.net/pypi/v/stpyvista"></a>
<a href="https://github.com/edsaac/stpyvista-tests"><img alt="stpyvista examples repository" src="https://img.shields.io/static/v1?label=:&message=Examples&color=ff4b4b&logo=github"></a>
<a href="https://stpyvista.streamlit.app"><img alt="Launch stpyvista in Streamlit" src="https://img.shields.io/static/v1?label=:&message=Open%20in%20Streamlit&color=pink&logo=streamlit"></a>
</p>

This is a simple component that takes a PyVista plotter object and shows it on Streamlit as an interactive element (as in it can be zoomed in/out, moved and rotated, but the visualization state is not returned). It uses PyVista's [panel backend](https://docs.pyvista.org/user-guide/jupyter/panel.html) and it basically takes the plotter, [exports it to HTML](https://docs.pyvista.org/api/plotting/_autosummary/pyvista.Plotter.export_html.html) and displays that within an iframe.

## Installation 

```sh
pip install stpyvista
```

## Check the demos

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stpyvista.streamlit.app/)


****

#### Also check:
* The PyVista project at [https://www.pyvista.org/](https://www.pyvista.org/)
* @blackary['s blog post](https://blog.streamlit.io/how-to-build-your-own-streamlit-component/) on how to build a custom component

