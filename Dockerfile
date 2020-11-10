FROM python:3.8-slim

WORKDIR /code

EXPOSE 8501

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["streamlit", "run", "./streamlit_app.py"]