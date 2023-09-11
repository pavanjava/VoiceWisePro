import os


def handle_upload_files(uploaded_file):
    if uploaded_file is not None:
        # uncomment below to display the file details
        # file_details = {"fileName": uploaded_file.name, "fileType": uploaded_file.type}
        # streamlit.write(file_details)
        tmp_file = os.path.join("/tmp", uploaded_file.name)
        with open(tmp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return tmp_file