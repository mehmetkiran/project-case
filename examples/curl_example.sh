# Register User

curl --location 'http://127.0.0.1:8000/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "password": "secure_password",
    "email":  "demo@acmeindustries.com"
}'


# Login User

curl --location 'http://127.0.0.1:8000/users/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "password": "secure_password",
    "email":  "demo@acmeindustries.com"
}'


# Upload File

curl --location 'http://127.0.0.1:8000/pdf/pdf-upload/' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--form 'file=@"sample.pdf"'


# List PDF

curl --location 'http://127.0.0.1:8000/pdf/pdf-list' \
--header 'Authorization: Bearer <JWT_TOKEN>'

# Parse PDF

curl --location 'http://127.0.0.1:8000/pdf/pdf-parse' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--data '{
    "pdf_id": "68379300d26107d549c9fb6b"
}'

# PDF Select

curl --location 'http://127.0.0.1:8000/pdf/pdf-select' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--data '{
    "pdf_id": "68379300d26107d549c9fb6b"
}'

# Chat History

curl --location 'http://127.0.0.1:8000/chat/chat-history' \
--header 'Authorization: Bearer <JWT_TOKEN>' \

# Chat Send
curl --location 'http://127.0.0.1:8000/chat/pdf-chat' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--data '{
  "message": "Can you explain this pdf?"
}'