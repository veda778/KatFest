from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

_generator = None

def get_generator():
    global _generator
    if _generator is None:
        model_name = "google/flan-t5-base"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        _generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )

    return _generator


def generate_answer(context, query):
    generator = get_generator()

    prompt = f"""
Answer the question using only the legal information below.
Keep the answer concise (2-4 sentences).

Legal Information:
{context}

Question:
{query}

Answer:
"""

    response = generator(
        prompt,
        max_length=200,
        do_sample=False
    )

    return response[0]["generated_text"].replace(prompt, "").strip()