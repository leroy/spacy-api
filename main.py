from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Taal NLP API", description="spaCy-based sentence and word detection for Taal game")

# Load Dutch model once at startup (not per request)
nlp = None


def load_model():
    global nlp
    if nlp is None:
        import spacy
        nlp = spacy.load("nl_core_news_sm")
    return nlp


@app.on_event("startup")
async def startup():
    load_model()


class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    doc = nlp(req.text)
    return {
        "sentences": [s.text.strip() for s in doc.sents],
        "words": [t.text for t in doc if not t.is_space],
        "tokens": [
            {"text": t.text, "pos": t.pos_, "lemma": t.lemma_}
            for t in doc
            if not t.is_space
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": "nl_core_news_sm"}
