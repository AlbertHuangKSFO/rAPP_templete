FROM python:3.13-slim

ARG USER_ID=60577
ARG USER_NAME="eric-sdk"
ARG APP_VERSION
LABEL \
    adp.app.version=$APP_VERSION

WORKDIR /code

COPY src/ ./src
COPY ./libs ./libs
COPY requirements.txt .
COPY .env .
COPY cerificates ./certificates
RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN echo "$USER_ID:x:$USER_ID:0:An Identity for $USER_NAME:/nonexistent:/bin/false" >>/etc/passwd
RUN echo "$USER_ID:!::0:::::" >>/etc/shadow

USER $USER_ID

CMD ["uvicorn", "src.server:app", "--host=0.0.0.0", "--port", "8050"]

