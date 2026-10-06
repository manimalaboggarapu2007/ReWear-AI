import streamlit as st

LABELS = [
    "a shirt",
    "a t-shirt",
    "jeans",
    "trousers",
    "a dress",
    "a skirt",
    "a jacket",
    "a sweater",
    "a hoodie",
    "shoes",
    "a clothing item",
    "a car",
    "food",
    "a person"
]

@st.cache_resource
def load_classifier():
    from transformers import pipeline
    return pipeline(
        "zero-shot-image-classification",
        model="openai/clip-vit-base-patch32"
    )

def classify_image(image):
    classifier = load_classifier()
    results = classifier(image, candidate_labels=LABELS)
    best = results[0]
    return {"label": best["label"], "score": best["score"] * 100}
