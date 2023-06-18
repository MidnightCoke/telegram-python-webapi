FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=server.py

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
