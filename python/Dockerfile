FROM registry.red-soft.ru/ubi7/ubi:latest

COPY Python-3.12.7.tgz /python-source/

RUN  dnf groupinstall -y 'Development Tools' && \
     dnf install -y openssl-devel bzip2-devel libffi-devel xz-devel zlib-devel sqlite-devel && \
     tar -zxvf /python-source/Python-3.12.7.tgz -C /python-source/ && \
     cd /python-source/Python-3.12.7 && \
     ./configure --enable-optimizations && \
     make altinstall && \
     rm -rf /python-source/Python-3.12.7 /python-source/Python-3.12.7.tgz  && \
     ln -s /usr/local/bin/pip3 /usr/local/bin/pip
ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
