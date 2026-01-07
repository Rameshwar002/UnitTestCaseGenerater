def extract_class_name(path):
    return path.split("/")[-1].replace(".java", "")

def extract_package_path(path, base):
    return path.split(base)[1].rsplit("/", 1)[0]

def find_missing_tests(main_files, test_files):
    test_index = {}

    for t in test_files:
        name = extract_class_name(t)
        pkg = extract_package_path(t, "src/test/java")
        test_index[(name, pkg)] = t

    missing = []

    for m in main_files:
        cls = extract_class_name(m)
        pkg = extract_package_path(m, "src/main/java")
        expected = f"{cls}Test"

        if (expected, pkg) not in test_index:
            missing.append({
                "class": cls,
                "package": pkg,
                "expected": f"{expected}.java",
                "source": m
            })

    return missing
