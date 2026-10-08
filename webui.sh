#!/bin/bash
pip install -r requirements.txt
PYTHONPATH=. streamlit run webui.py
