from python:3.9.7

WORKDIR /usr/src/application

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "fastapiapp.main:app", "--host", "0.0.0.0", "--port", "8000"]