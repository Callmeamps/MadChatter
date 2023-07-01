FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /madchatter

COPY ./requirements.txt /madchatter
RUN python3 -m pip install --no-cache-dir -r requirements.txt
    
RUN playwright install-deps

RUN playwright install chromium

COPY . /madchatter

EXPOSE 8080

CMD [ "chainlit" , "run", "-h", "app.py"]
