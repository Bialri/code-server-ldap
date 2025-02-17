FROM debian:12

COPY code-marketplace-linux-arm64 /code/
COPY run.sh /code/
RUN mkdir /root/extentions

ENTRYPOINT ["/code/run.sh"]