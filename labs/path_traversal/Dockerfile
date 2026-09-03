FROM python:3.12-slim

WORKDIR /lab

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    -r requirements.txt

COPY app ./app
COPY data ./data

RUN useradd \
    --create-home \
    --uid 1001 \
    labuser \
    && chown -R labuser:labuser /lab

USER 1001

EXPOSE 8000

CMD ["uvicorn", \
    "app.main:app", \
    "--host", \
    "0.0.0.0", \
    "--port", \
    "8000" \
]