Write-Host "Starting Kiosk Wizard..."
clear
python3 -m pip install -r requirements.txt
clear
python3 screexy.py kiosk wizard
clear
python3 screexy.py tools thumbnail