import streamlit as st
import os
from dotenv import load_dotenv
from utils import safe_write, safe_read

load_dotenv()

from chains import (
    design_chain,
    file_structure_chain,
    file_path_chain,
    code_chain,
)

st.title("Code Generator")

language = st.radio("Select Language:",
                    ["Python", "Java", "C#", "TypeScript", "Rust", "Kotlin"])
request = st.text_area('Please Detail Your Desired Use Case for Code Generation! ', height=500)

app_name = st.text_input('Enter Project Name:')
submit = st.button("submit", type="primary")


if language and submit and app_name:

    dir_path = app_name + '/'

    design = design_chain.run({'language': language, 'input': request})
    design_doc_path = dir_path + '/design' + '/design.txt'
    safe_write(design_doc_path, design)
    st.markdown(""" :blue[Technical Design : ] """, unsafe_allow_html=True)
    st.write(design)

    file_structure = file_structure_chain.run({'language': language, 'input': design})
    file_structure_path = dir_path + '/file_structure' + '/file_structure.txt'
    safe_write(file_structure_path, file_structure)
    st.markdown(""" :blue[File Names :] """, unsafe_allow_html=True)
    st.write(file_structure)

    files = file_path_chain.run({'language': language, 'input': file_structure})
    files_path = dir_path + '/files' + '/files.txt'
    safe_write(files_path, files)
    st.markdown(""" :blue[File Paths :] """, unsafe_allow_html=True)
    st.write(files)

    # read the files from the file path
    # files_path = dir_path + '/files' + '/files.txt'
    # files = safe_read(files_path)

    files_list = files.split('\n')

    # design = safe_read(dir_path + '/design' + '/design.txt')

    for file in files_list:
        # skip file name with ```
        if file.startswith('```'):
            continue
        code_path = os.path.join(dir_path, 'code', file)
        norm_code_path = os.path.normpath(code_path)
        st.markdown(f""" :blue[Generating code for {file} :] """, unsafe_allow_html=True)
        code = code_chain.predict(language=language, file=file, design=design)
        safe_write(norm_code_path, code)
        st.write(code)
