#!/bin/bash

if [ ! -d /home/coder/.local ]; then
  mkdir /home/coder/.local && mkdir /home/coder/.local/lib && mkdir /home/coder/.local/bin
  tar -C /home/coder/.local/lib -xzf /code/code-server-4.96.4-linux-arm64.tar.gz
  mv /home/coder/.local/lib/code-server-4.96.4-linux-arm64 /home/coder/.local/lib/code-server-4.96.4
  ln -s /home/coder/.local/lib/code-server-4.96.4/bin/code-server /home/coder/.local/bin/code-server

  export EXTENSIONS_GALLERY='{"serviceUrl":"http://registry:3001/api", "itemUrl":"http://registry:3001/item", "resourceUrlTemplate": "http://registry:3001/files/{publisher}/{name}/{version}/{path}"}'

  parallel ::: 'python3 /code/network_usage.py' '/home/coder/.local/bin/code-server --bind-addr 0.0.0.0:8080'
else
  mv /home/coder/.local/lib/code-server-4.96.4-linux-arm64 /home/coder/.local/lib/code-server-4.96.4
  ln -s /home/coder/.local/lib/code-server-4.96.4/bin/code-server /home/coder/.local/bin/code-server
  export EXTENSIONS_GALLERY='{"serviceUrl":"http://registry:3001/api", "itemUrl":"http://registry:3001/item", "resourceUrlTemplate": "http://registry:3001/files/{publisher}/{name}/{version}/{path}"}'

  parallel ::: 'python3 /code/network_usage.py' '/home/coder/.local/bin/code-server --bind-addr 0.0.0.0:8080'
fi

