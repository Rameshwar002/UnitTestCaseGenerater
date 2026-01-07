import zipfile
import tempfile
import os

def extract_zip(uploaded_zip):
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, uploaded_zip.name)

    with open(zip_path, "wb") as f:
        f.write(uploaded_zip.getbuffer())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    return temp_dir
