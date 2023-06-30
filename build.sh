pip install -r requirements.txt
playwright install
python -m chainlit run -h app.py --host 0.0.0.0 --port 8080