Write-Host "Starting Kiosk Wizard..."
clear
python3 -m pip install -r requirements.txt
clear
python3 viexly.py kiosk wizard
clear
python3 viexly.py tools thumbnail