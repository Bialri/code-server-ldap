#!/bin/bash

/code/code-marketplace-linux-arm64 add /extentions --extensions-dir /root/extentions

/code/code-marketplace-linux-arm64 server --address 0.0.0.0:3001 --extensions-dir /root/extentions