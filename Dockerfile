FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN python3.12 -m pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "comodoro.py"]