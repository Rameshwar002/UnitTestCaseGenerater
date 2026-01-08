import streamlit as st
import time
import pandas as pd

from core.zip_handler import extract_zip
from core.java_scanner import scan_java_files
from core.test_matcher import find_missing_tests
from core.class_classifier import classify
from llm.junit_generator import generate_test
from utils.path_utils import build_test_path
from core.test_aggregator import create_test_bundle


def run_app():
    st.set_page_config(page_title="MicroTestIQ", layout="wide")

    st.title("🧪 MicroTestIQ – Enterprise Unit Test Generator")
    st.caption("Batch • Status Tracking • Audit Ready")

    # --------------------------------------------------
    # Session State Initialization (IMPORTANT)
    # --------------------------------------------------
    if "table" not in st.session_state:
        st.session_state.table = None

    if "test_zip" not in st.session_state:
        st.session_state.test_zip = None

    if "generated_tests" not in st.session_state:
        st.session_state.generated_tests = []

    # --------------------------------------------------
    # Upload ZIP
    # --------------------------------------------------
    zip_file = st.file_uploader("Upload Microservices ZIP", type=["zip"])
    if not zip_file:
        return

    # --------------------------------------------------
    # STEP 1: Extract & Scan
    # --------------------------------------------------
    root = extract_zip(zip_file)
    main_files, test_files = scan_java_files(root)
    missing = find_missing_tests(main_files, test_files)

    if not missing:
        st.success("🎉 All files already have unit tests")
        return

    st.subheader("🚨 Application Files Without Unit Tests")

    # --------------------------------------------------
    # STEP 2: Initialize Table
    # --------------------------------------------------
    if st.session_state.table is None:
        st.session_state.table = pd.DataFrame([
            {
                "File Name": f"{m['class']}.java",
                "File Path": m["source"].replace(root, ""),
                "Status": "⏳ Pending",
                "Remarks": ""
            }
            for m in missing
        ])

    table_placeholder = st.empty()
    table_placeholder.dataframe(
        st.session_state.table,
        use_container_width=True
    )

    # --------------------------------------------------
    # STEP 3: Batch Generation
    # --------------------------------------------------
    if st.button("🚀 Generate Test Cases (Auto)"):
        progress = st.progress(0)
        total = len(missing)

        st.session_state.generated_tests = []

        for i, item in enumerate(missing):
            cls = item["class"]
            src = item["source"]

            # Update status → In Progress
            st.session_state.table.loc[
                st.session_state.table["File Name"] == f"{cls}.java",
                "Status"
            ] = "⚙ In Progress"

            table_placeholder.dataframe(
                st.session_state.table,
                use_container_width=True
            )

            try:
                with open(src, "r", encoding="utf-8") as f:
                    java_code = f.read()

                class_type = classify(java_code)

                test_code = generate_test(
                    java_code=java_code,
                    class_name=cls,
                    class_type=class_type
                )

                test_path = build_test_path(
                    root,
                    item["package"],
                    cls
                )

                with open(test_path, "w", encoding="utf-8") as f:
                    f.write(test_code)

                st.session_state.generated_tests.append({
                    "path": test_path,
                    "content": test_code
                })

                # Update status → Done
                st.session_state.table.loc[
                    st.session_state.table["File Name"] == f"{cls}.java",
                    ["Status", "Remarks"]
                ] = ["✅ Done", "Test generated successfully"]

            except Exception as e:
                # Update status → Failed
                st.session_state.table.loc[
                    st.session_state.table["File Name"] == f"{cls}.java",
                    ["Status", "Remarks"]
                ] = ["❌ Failed", str(e)]

            progress.progress((i + 1) / total)
            table_placeholder.dataframe(
                st.session_state.table,
                use_container_width=True
            )

            time.sleep(0.2)

        # --------------------------------------------------
        # STEP 4: Create ZIP (IN MEMORY)
        # --------------------------------------------------
        if st.session_state.generated_tests:
            st.session_state.test_zip = create_test_bundle(
                root,
                st.session_state.generated_tests
            )

        st.success("✅ Batch generation completed")

    # --------------------------------------------------
    # STEP 5: Download ZIP (FIXED & RELIABLE)
    # --------------------------------------------------
    if st.session_state.test_zip is not None:
        st.download_button(
            label="⬇ Download All Unit Tests",
            data=st.session_state.test_zip,
            file_name="all-unit-tests.zip",
            mime="application/zip"
        )


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    run_app()
