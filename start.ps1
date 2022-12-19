# Check if python 3.9 is installed
$python = (Get-Command python3.9) -eq $null

# If python 3.9 is not installed, install it
if (-not $python) {
    # Install python 3.9
    Invoke-WebRequest -Uri 
"https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe" -OutFile 
"python-3.9.1-amd64.exe"
    Start-Process -FilePath ".\python-3.9.1-amd64.exe" -ArgumentList 
'/quiet InstallAllUsers=1 PrependPath=1' -Wait
    Remove-Item -Path ".\python-3.9.1-amd64.exe"
}

# Create a virtual environment with python 3.9
python3.9 -m venv env

# Activate the virtual environment
.\env\scripts\activate.ps1

# Install the requirements from the requirements.txt file
pip install -r requirements.txt

python manage.py makemigrations backend
# Run Django migrations
python manage.py migrate

# Start browser
Start-Process -Verb Open "http://localhost:8000/"

# Start the Django development server
python manage.py runserver
