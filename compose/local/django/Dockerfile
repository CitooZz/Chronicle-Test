FROM python:3.9.10
ENV PYTHONUNBUFFERED 1
RUN apt-get update
ADD chronicle/requirements.txt chronicle/requirements.txt
RUN pip install --no-cache-dir -r chronicle/requirements.txt

COPY ./compose/local/django/entrypoint /entrypoint
COPY ./compose/local/django/start /start
RUN chmod +x /entrypoint /start

ADD .env/.local/.django /envs/

# Mount your repo root dire as a volume under /code
RUN mkdir /code
WORKDIR /code

ENTRYPOINT ["/entrypoint"]