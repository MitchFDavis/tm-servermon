# tm-servermon
PyPlanet project to read and report server events without messing with existing server controllers

Requires Python 3.8. Server connection details can be edited in settings/base.py. Main logic is in apps/gamestats/\_\_init\_\_.py.

To set up:  
```
python3.8 -m venv pyplanet-env
source pyplanet-env/bin/activate
pip install -r requirements.txt
./manage.py start
```
