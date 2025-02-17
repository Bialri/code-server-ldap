FROM debian:12

RUN adduser --disabled-password --gecos "" coder

COPY code-server-4.96.4-linux-arm64.tar.gz /code/


COPY run.sh /code/
RUN mkdir /home/coder/.local && mkdir /home/coder/.local/lib && mkdir /home/coder/.local/bin \
    && tar -C /home/coder/.local/lib -xzf /code/code-server-4.96.4-linux-arm64.tar.gz \
    && mv /home/coder/.local/lib/code-server-4.96.4-linux-arm64 /home/coder/.local/lib/code-server-4.96.4 \
    && ln -s /home/coder/.local/lib/code-server-4.96.4/bin/code-server /home/coder/.local/bin/code-server \
    && PATH="/home/coder/.local/bin:$PATH" \
    && chmod -R 777 /home/coder

USER coder

RUN PATH="/home/coder/.local/bin:$PATH"
EXPOSE 8080
ENTRYPOINT ["/code/run.sh"]