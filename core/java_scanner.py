import os

def scan_java_files(root):
    main_files = []
    test_files = []

    for r, _, files in os.walk(root):
        for f in files:
            if f.endswith(".java"):
                path = os.path.join(r, f).replace("\\", "/")

                if "src/main/java" in path:
                    main_files.append(path)

                elif "src/test/java" in path:
                    test_files.append(path)

    return main_files, test_files
