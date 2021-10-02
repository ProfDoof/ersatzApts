FROM python:3.9-buster AS base

FROM base AS builder

WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base AS runner

ENV FLASK_APP app.py
WORKDIR /project
COPY --from=builder /install /usr/local
ADD . /project

EXPOSE 80
EXPOSE 9191
CMD [ "uwsgi", "--http=0.0.0.0:80", "--wsgi-file=app.py", "--callable=app", "--processes=4", "--threads=2", "--http=0.0.0.0:9191" ]