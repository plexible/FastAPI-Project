# FastAPI Project

This project includes a web feature developed through [FastAPI](https://fastapi.tiangolo.com/). You can perform various operations in the project using GET and POST requests.

## Beginning
You can start by cloning the project.
```console
git clone https://github.com/plexible/stAPI-Project.git
cd FastAPI-Project
```

## Requirements
Some requirements are needed for the project to work.
1. requirements.txt file:
```console
pip install -r requirements.txt
```

2. The EmbeddingExtractingPart.py file should be downloaded from the GitHub repository. This file is the python file required for the Secure Data Transfer and Information Hiding Project:
```console
mkdir project_documents
cd project_documents
curl -o EmbeddingExtractingPart.py -k https://raw.githubusercontent.com/plexible/Hide-Encrypted-Information-Into-GrayScale-Image/main/EmbeddingExtractingPart.py
```

3. Utilizing the trained model and scaling for deployment through Google Drive:
```console
cd project_documents
curl -L -o random_forest_model.joblib --insecure "https://drive.google.com/uc?id=1DJiLSUX-Isjv4VdZjDJIMEmo5EvJQKPx"
curl -L -o scaler.joblib --insecure "https://drive.google.com/uc?id=1grLimRCqcz0LsUenNjyELT-suvO1Cn_F"
```

## Use
To run project:
```console
uvicorn app:app --reload
```
