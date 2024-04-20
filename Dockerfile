FROM python:3.9 as python-base


ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/opt/.cache

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /eduki

# Copy Project Files
COPY . .

WORKDIR /eduki/eduki_data_engineering

RUN chmod -R 755 .

# Install Dependencies
RUN poetry install --no-interaction --no-cache 

# CMD ["poetry", "run", "python", "bq.py"]
# ENTRYPOINT ["poetry", "run"]
CMD ["tail", "-f", "/dev/null"]




