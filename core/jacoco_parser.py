import xml.etree.ElementTree as ET

def parse_jacoco(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    report = []

    for pkg in root.findall(".//package"):
        for cls in pkg.findall("class"):
            name = cls.attrib["name"].replace("/", ".")
            counter = cls.find("counter[@type='LINE']")
            covered = int(counter.attrib["covered"])
            missed = int(counter.attrib["missed"])

            report.append({
                "class": name,
                "coverage": round(
                    covered / (covered + missed) * 100, 2
                )
            })

    return report
