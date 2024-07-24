# resume-criteria-api

# curl command

curl -X POST "http://127.0.0.1:8000/process-pdf" \
-H "Content-Type: multipart/form-data" \
-F "file=@example.pdf" \
-F "criteria=Your criteria here"
