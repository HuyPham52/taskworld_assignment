FROM python:3.8-slim

ENV SRC_DIR /opt/app
WORKDIR $SRC_DIR

# Copy data
COPY resources/ /opt
# Copy functions to run job
COPY ./src/main.py $SRC_DIR
COPY .env_stag $SRC_DIR/.env

COPY requirements.txt $SRC_DIR

RUN pip install -r requirements.txt

# ENTRYPOINT ["python", "-V"]
ENTRYPOINT [ "python", "main.py", "--source", "/opt/data/activity.csv", "--database", "warehouse", "--table", "user_activity" ]
