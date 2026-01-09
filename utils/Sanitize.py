import re


def sanitize_test_code(raw_code: str, class_name: str) -> str:
    """
    Cleans LLM output to ensure:
    - Only Java code
    - Single public test class
    - No markdown or explanations
    """

    # ----------------------------------
    # Remove markdown blocks
    # ----------------------------------
    raw_code = re.sub(r"```java", "", raw_code, flags=re.IGNORECASE)
    raw_code = re.sub(r"```", "", raw_code)

    # ----------------------------------
    # Remove common LLM explanations
    # ----------------------------------
    noise_patterns = [
        r"^Sure.*?\n",
        r"^Here is.*?\n",
        r"Hope this helps.*",
        r"Let me know.*",
    ]

    for p in noise_patterns:
        raw_code = re.sub(p, "", raw_code, flags=re.IGNORECASE | re.DOTALL)

    # ----------------------------------
    # Extract package + imports
    # ----------------------------------
    package_match = re.search(r"(package\s+[\w\.]+;)", raw_code)
    imports = re.findall(r"(import\s+[\w\.\*]+;)", raw_code)

    package_line = package_match.group(1) if package_match else ""
    import_block = "\n".join(imports)

    # ----------------------------------
    # Extract ONLY the correct public test class
    # ----------------------------------
    class_pattern = rf"(public\s+class\s+{class_name}Test\s*\{{[\s\S]*?\}})"
    class_match = re.search(class_pattern, raw_code)

    if not class_match:
        raise ValueError("Valid public test class not found in LLM output")

    class_body = class_match.group(1)

    # ----------------------------------
    # Rebuild clean Java file
    # ----------------------------------
    clean_code = "\n\n".join(
        part for part in [
            package_line,
            import_block,
            class_body
        ] if part.strip()
    )

    return clean_code.strip()
