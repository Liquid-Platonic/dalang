FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

RUN apt update && apt install libopus0

RUN poetry install
RUN pip3 install torchaudio==0.11.0
RUN python -m nltk.downloader words
RUN mkdir temp

CMD [ "python3", "dalang/discordbot/main.py" ]