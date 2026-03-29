    FROM python:3.12

    WORKDIR /cash-control

    COPY pyproject.toml poetry.lock ./

    RUN pip install poetry && poetry config virtualenvs.create false \ 
        && poetry install --no-root

    COPY . .

    CMD ["uvicorn", "cash_control.main:app", "--host", "0.0.0.0", "--port", "8000"]