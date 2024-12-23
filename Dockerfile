FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV BASE_PATH=/app/media \
    INPUT_FORMAT=m2ts \
    OUTPUT_FORMAT=mp4 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VENV="/opt/poetry-venv" \
    POETRY_CACHE_DIR="/opt/.cache"

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

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
CMD ["-d", "$BASE_PATH", "-i", "$INPUT_FORMAT", "-o", "$OUTPUT_FORMAT"]

