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
python -m management-console-backend.src.main
```
#### Run Simulator
```
python .\management-console-backend\src\event_simulator.py
```
# Test 
```
pytest -v management-console-backend/tests/test_api.py
```