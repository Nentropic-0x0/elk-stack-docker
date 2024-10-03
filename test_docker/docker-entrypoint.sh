#!/bin/sh
set -e

echo "Elasticsearch host: ${ELASTICSEARCH_HOST}"
echo "Elasticsearch port: ${ELASTICSEARCH_PORT}"

until curl -s -f -o /dev/null "http://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}"; do
    echo "Waiting for Elasticsearch at ${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}..."
    sleep 5
done
echo "Elasticsearch is up - executing command"

exec "$@"