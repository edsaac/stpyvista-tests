import pyvista as pv
import streamlit as st
from stpyvista import stpyvista, HTML_stpyvista
import tempfile

def delmodel(): 
    del st.session_state.model
    del st.session_state.fileuploader

## Streamlit layout
st.title("STL viewer")
placeholder = st.empty()

with placeholder:
    uploadedFile = st.file_uploader(
        "Upload a STL file:",
        ["stl"],
        accept_multiple_files=False,
        key="fileuploader")

if uploadedFile:
    
    # Storing the threejs models as a session_state variable
    # allows to avoid rerendering at each time something changes
    # in the page
    if "model" not in st.session_state:
        
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

            ## Export to a pythreejs HTML
            st.session_state.model = HTML_stpyvista(plotter)
        
    ## Show in webpage
    with placeholder.container():
        st.button("Restart", "btn_rerender", on_click=delmodel)
        stpyvista(st.session_state.model)
    