import os
import zipfile
import tempfile
from core.test_collector import collect_existing_tests

def create_test_bundle(project_root, generated_tests):
    temp_dir = tempfile.mkdtemp()
    test_root = os.path.join(temp_dir, "src/test/java")
    os.makedirs(test_root, exist_ok=True)

    collect_existing_tests(project_root, test_root)

    for test in generated_tests:
        os.makedirs(os.path.dirname(test["path"]), exist_ok=True)
        with open(test["path"], "w") as f:
            f.write(test["content"])

    zip_path = os.path.join(temp_dir, "all-unit-tests.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for r, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".java"):
                    full = os.path.join(r, file)
                    zipf.write(full, full.replace(temp_dir + "/", ""))

    return zip_path
