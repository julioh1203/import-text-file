FROM python:3.10.8-slim-bullseye AS app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && useradd --create-home python \
    && chown python:python -R /app \
    && mkdir /static \
    && chown python:python -R /static

USER python

COPY --chown=python:python . .

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="/app" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python" \
    DJANGO_SETTINGS_MODULE="importation.settings"

RUN python -m pip install install /app gunicorn

RUN if [ "${DEBUG}" = "false" ]; then \
    SECRET_KEY=dummyvalue python manage.py collectstatic --no-input; \
    fi

ENTRYPOINT ["/app/docker/entrypoint.sh"]

RUN chmod +x /app/docker/entrypoint.sh

EXPOSE 8000

CMD ["python -m gunicorn", "-c", "python:importation.gunicorn", "importation.wsgi"]
