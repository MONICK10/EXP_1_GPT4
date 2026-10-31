# Runs the app with Ollama, captures all screenshots + demo video, and builds this experiment's record PDF.
# Run:  .\make_record.ps1
if (Test-Path ..\.venv) { . ..\.venv\Scripts\Activate.ps1 } elseif (Test-Path .venv) { . .\.venv\Scripts\Activate.ps1 }
python tools\capture.py
python tools\build_record.py
Write-Host "Done! Open Exp1_Record_URK23CS1167.pdf and the videos folder." -ForegroundColor Green
