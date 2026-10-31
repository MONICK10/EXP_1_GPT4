# One-time setup on Windows (PowerShell).  Run:  .\setup.ps1
# If scripts are blocked, first run:  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Write-Host "1/4 Creating virtual environment..." -ForegroundColor Cyan
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
Write-Host "2/4 Installing Python packages (takes a few minutes)..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "3/4 Installing Chromium for screenshots/videos..." -ForegroundColor Cyan
python -m playwright install chromium
Write-Host "4/4 Pulling the Llama 3.2 model in Ollama (about 2 GB)..." -ForegroundColor Cyan
ollama pull llama3.2
Write-Host "Setup done. Next run:  .\make_record.ps1" -ForegroundColor Green
