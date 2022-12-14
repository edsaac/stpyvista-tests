import pyvista as pv
import streamlit as st
import tempfile
from stpyvista import stpyvista

st.set_page_config(page_icon="🧊", layout="wide")

# Add badges to sidebar
with st.sidebar:
    with open("assets/badges.md") as f:
        st.markdown(f"""{f.read()}""", unsafe_allow_html=True)

def delmodel(): 
    del st.session_state.fileuploader

## Streamlit layout
st.title("📤   Upload a STL file")
placeholder = st.empty()

with placeholder:
    uploadedFile = st.file_uploader(
        "Upload a STL file:",
        ["stl"],
        accept_multiple_files=False,
        key="fileuploader")

if uploadedFile:
    
    ## Initialize pyvista reader and plotter
    plotter = pv.Plotter(border=False, window_size=[500,400]) 
    plotter.background_color = "white"

    ## Create a tempfile to keep the uploaded file as pyvista's API 
    ## only supports file paths but not buffers
    with tempfile.NamedTemporaryFile(suffix="_streamlit") as f: 
        f.write(uploadedFile.getbuffer())
        reader = pv.STLReader(f.name)
    
        ## Read data and send to plotter
        mesh = reader.read()
        plotter.add_mesh(mesh,color="salmon")
        plotter.view_isometric()

    ## Show in webpage
    with placeholder.container():
        st.button("Restart", "btn_rerender", on_click=delmodel)
        stpyvista(plotter, key="my_stl")
    