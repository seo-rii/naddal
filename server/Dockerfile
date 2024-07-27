FROM python:3.11-slim
WORKDIR /app
COPY . /app

RUN chmod +x /app/run.sh

VOLUME [ "/app/uploads", "/app/mark" ]

RUN mkdir -p /app/uploads /app/mark

RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT [ "/app/run.sh" ]
