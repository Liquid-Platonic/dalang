FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN poetry install
RUN poetry shell

RUN pip3 install torchaudio==0.11.0

#CMD [ "python3", "dalang/discordbot/main.py" ]