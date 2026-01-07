import os

def build_test_path(root, package, class_name):
    base = os.path.join(
        root,
        "src/test/java",
        package.strip("/")
    )

    os.makedirs(base, exist_ok=True)

    return os.path.join(base, f"{class_name}Test.java")
