pip install -r requirements.txt
sudo snap install ollama
ollama pull mxbai-embed-large

### Run Server

Simply run
```
cd python-core
fastapi dev server.py
```