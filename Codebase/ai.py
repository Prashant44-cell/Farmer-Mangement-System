import ollama

def generate_ollama_suggestion(prompt):
    try:
        return ollama.generate(
            model="phi3",
            prompt=prompt,
            stream=True,
            options={"temperature": 0.7, "max_tokens": 300},
        )
    except Exception as e:
        return [{"response": f"Ollama Error: {str(e)}"}]
