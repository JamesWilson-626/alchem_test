# Alchem Test
---
# Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
---
# Run
#### Start API & Database
```
python main.py
```
#### Run Simulator
```
python event_simulator.py
```
---
# Test 
```
pytest -v management_console/tests/test_api.py
```