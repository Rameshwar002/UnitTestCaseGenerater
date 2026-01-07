junit_prompt = """
You are a Senior Java Test Architect.

Generate JUnit 5 test cases.

Class Type: {class_type}
Class Name: {class_name}

Rules:
- Use Mockito if dependencies exist
- Follow AAA pattern
- Cover success, failure, edge cases
- Use @WebMvcTest for Controllers
- Use @SpringBootTest for Services
- Achieve 90%+ coverage

Java Source:
{java_code}
"""
