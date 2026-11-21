ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apk add --no-cache python3
WORKDIR /app
COPY receiver.py /app/receiver.py
RUN chmod 0644 /app/receiver.py
CMD ["/usr/bin/with-contenv", "python3", "/app/receiver.py"]
