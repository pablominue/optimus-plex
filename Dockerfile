FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV BASE_PATH="/app/data" \
    INPUT_FORMAT="mp4" \
    OUTPUT_FORMAT="mkv" \
    POETRY_VENV="/opt/poetry-venv" \
    PLEX_URL="http://localhost:32400" \
    PLEX_TOKEN="" \
    DELETE_OLD="True" 

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Instala las dependencias del proyecto
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copia el resto del código fuente
COPY . .

# Comando para ejecutar la aplicación
ENTRYPOINT ["poetry", "run", "python3", "optimus-plex"]


