def classify(java_code: str):
    if "@RestController" in java_code or "@Controller" in java_code:
        return "CONTROLLER"
    if "@Service" in java_code:
        return "SERVICE"
    if "@Repository" in java_code:
        return "REPOSITORY"
    return "UTILITY"
