# apt update && apt install python3 -y
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python3 get-pip.py
# python3 -m pip install -r requirements.txt
playwright install-deps
playwright install 
# python3 -m chainlit run -h app.py --host 0.0.0.0 --port 8080