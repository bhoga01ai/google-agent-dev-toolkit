#!/bin/bash

ACCESS_TOKEN=$(gcloud auth print-access-token)
echo "Access Token: $ACCESS_TOKEN"

# Reasoning engine endpoint URL
#ENDPOINT_URL="https://us-central1-aiplatform.googleapis.com/v1/projects/myproject-454701/locations/us-central1/reasoningEngines/8604342592370376704:streamQuery?alt=sse"

ENDPOINT_URL="https://us-central1-aiplatform.googleapis.com/v1/projects/myproject-454701/locations/us-central1/reasoningEngines/8604342592370376704:streamQuery"

echo "Calling streamQuery endpoint..."
curl -X POST \
-H "Authorization: Bearer ${ACCESS_TOKEN}" \
-H "Content-Type: application/json" \
"${ENDPOINT_URL}" \
-d '{
  "input": {
    "text": "What is the exchange rate from US dollars to Swedish currency?"
  }
}'
