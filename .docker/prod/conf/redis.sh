#!/bin/bash

mkdir -p /usr/local/etc/redis

echo "aclfile /usr/local/etc/redis/custom_aclfile.acl" > /usr/local/etc/redis/redis.conf

if [ -n ${REDIS_USERNAME} ] && [ -n ${REDIS_PASSWORD} ]; then
    echo "user ${REDIS_USERNAME} on allkeys allchannels allcommands >${REDIS_PASSWORD} " > /usr/local/etc/redis/custom_aclfile.acl
fi

if [ $(echo ${REDIS_DISABLE_DEFAULT_USER}) == "true" ]; then
    echo "user default off nopass nocommands" >> /usr/local/etc/redis/custom_aclfile.acl
fi

exec docker-entrypoint.sh redis-server /usr/local/etc/redis/redis.conf