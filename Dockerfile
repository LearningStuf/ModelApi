FROM python:3.10-slim

Run pip install fastapi uvicorn scikit-learn==1.1.2 httpx pytest pyjwt passlib python-dotenv SQLAlchemy

COPY ./app /app

RUN mkdir -p /logs

ENV PYTHONPATH "${PYTHONPATH}:/app/"

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0" , "--port", "15400" ]  