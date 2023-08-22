FROM python:3.9-alpine

WORKDIR /mycarapp

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
#ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host=0.0.0.0"]

#docker build -t my-flask-app .
#docker run -p 5000:5000 my-flask-app