# Taal NLP API

spaCy-based sentence and word detection for the Taal Godot game. Uses the Dutch model (`nl_core_news_sm`).

## Local development

```bash
cd spacy-api
pip install -r requirements.txt
python -m spacy download nl_core_news_sm
uvicorn main:app --reload
```

API will be at http://127.0.0.1:8000. Try:

```bash
curl -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d "{\"text\": \"Hallo, hoe gaat het? Dit is een test.\"}"
```

## Deploy to Railway

1. Install [Railway CLI](https://docs.railway.app/develop/cli) or use the [dashboard](https://railway.app).
2. From the `taal` project root:
   ```bash
   cd spacy-api
   railway init
   railway up
   ```
3. Or: Push to GitHub, connect the repo in Railway, set the **Root Directory** to `spacy-api`, and deploy.
4. Railway will use `nixpacks.toml` to install deps and the spaCy model during build.

## API

- `POST /analyze` — Body: `{"text": "Your Dutch text here"}`  
  Returns: `{ "sentences": [...], "words": [...], "tokens": [...] }`
- `GET /health` — Health check

## Godot usage

```gdscript
const API_URL = "https://your-app.up.railway.app/analyze"

func analyze_text(text: String) -> void:
    var json_body = JSON.stringify({"text": text})
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(_on_analyze_complete.bind(request))
    request.request(API_URL, ["Content-Type: application/json"], HTTPClient.METHOD_POST, json_body)

func _on_analyze_complete(result: int, _code: int, _headers: PackedStringArray, body: PackedByteArray, request: HTTPRequest):
    request.queue_free()
    if result == HTTPRequest.RESULT_SUCCESS:
        var response = JSON.parse_string(body.get_string_from_utf8())
        print("Sentences: ", response.sentences)
        print("Words: ", response.words)
```
