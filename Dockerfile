FROM python:3.11


WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client

ENV PYTHONPATH=/app

RUN useradd -m app
RUN chown -R app:app /app

COPY --chown=app:app requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

USER app

COPY --chown=app:app . .
