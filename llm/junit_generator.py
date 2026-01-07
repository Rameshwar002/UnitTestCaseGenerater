import ollama
from llm.prompt_templates import junit_prompt

def generate_test(java_code, class_name, class_type):
    prompt = junit_prompt.format(
        class_name=class_name,
        class_type=class_type,
        java_code=java_code
    )

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]
