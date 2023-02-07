FROM python:3.9-slim
WORKDIR /

ENV PYTHONPATH=/backend

COPY backend /backend

#COPY ./alembic.ini /backend/alembic.ini

RUN python -m pip install --upgrade pip
RUN pip install -r /backend/requirements.txt


CMD ["python", "backend/api/main.py"]
