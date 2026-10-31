# Start this app (Ollama must be running).   .\run.ps1
if (Test-Path ..\.venv) { . ..\.venv\Scripts\Activate.ps1 } elseif (Test-Path .venv) { . .\.venv\Scripts\Activate.ps1 }
Start-Process "http://localhost:5001"
python app.py
