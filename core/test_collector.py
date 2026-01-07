import os
import shutil

def collect_existing_tests(root, output_dir):
    for r, _, files in os.walk(root):
        for f in files:
            if f.endswith("Test.java") and "src/test/java" in r.replace("\\", "/"):
                src = os.path.join(r, f)
                dst = os.path.join(output_dir, f)
                shutil.copy(src, dst)
