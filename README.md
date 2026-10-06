# ♻️ ReWear AI — Smart Wardrobe Reuse Platform

ReWear AI is an AIML-based wardrobe management and reuse platform. It helps users upload clothing images, classify clothing using a pre-trained CLIP model, store wardrobe information, generate basic outfit recommendations, track wear history, and identify least-worn items.

## Features
- Clothing image upload
- AI zero-shot image classification using CLIP
- Wardrobe database using SQLite
- Searchable wardrobe
- Wear-count tracking
- Weather/occasion/style-based outfit filtering
- Sustainability/reuse dashboard
- Responsive Streamlit interface

## Technology Stack
- Python
- Streamlit
- PyTorch
- Hugging Face Transformers
- OpenAI CLIP
- Pillow
- SQLite

## Run
```bash
python -m venv venv
# Windows PowerShell:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate

pip install -r requirements.txt
python -m streamlit run app.py
```

The first AI analysis downloads the CLIP model and may take some time.

## Project Structure
```
ReWear_AI/
├── app.py
├── ai_model.py
├── database.py
├── requirements.txt
├── README.md
├── data/
├── assets/
└── rag/
```

## Academic Note
This is a prototype. CLIP performs zero-shot classification rather than specialized garment segmentation or fine-grained fashion recognition. A production version could add a fashion-specific detector/classifier, user authentication, cloud storage, live weather APIs, and personalized recommendation models.
