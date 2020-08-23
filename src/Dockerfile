FROM python:3.6-alpine
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN pip install -e .

CMD [ "python", "./py_agent/main.py" ]