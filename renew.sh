#!/bin/bash
certbot renew --quiet --no-self-upgrade
if [ $? -eq 0 ]; then
    nginx -s reload
fi