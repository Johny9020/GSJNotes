FROM python:3.12-alpine

WORKDIR /gsjnotes

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Install psycopg2 for PostgreSQL connection
RUN apk update && apk add --no-cache postgresql-dev gcc musl-dev
RUN pip install psycopg2-binary

COPY . .

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]