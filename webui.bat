@echo off
pip install -r requirements.txt
set PYTHONPATH=.
streamlit run webui.py
pause
