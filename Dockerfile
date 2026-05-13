FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY QuickPay/pyproject.toml QuickPay/uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache -r pyproject.toml \
    && pip install --no-cache-dir gunicorn

COPY QuickPay .

RUN mkdir -p /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn QuickPay.wsgi:application --bind 0.0.0.0:8000"]
