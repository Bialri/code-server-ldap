FROM registry.red-soft.ru/ubi7/ubi:latest



COPY code-server-4.96.4-linux-amd64.tar.gz /code/
RUN tar -xzf /code/code-server-4.96.4-linux-amd64.tar.gz -C /code/ && \
    adduser -u 1000 --disabled-password --gecos "" edkardasov
USER edkardasov

ENTRYPOINT ["/code/code-server-4.96.4-linux-amd64/bin/code-server", "--bind-addr", "0.0.0.0:8080"]
