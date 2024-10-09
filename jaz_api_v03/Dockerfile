FROM python:3.11.4-slim-bullseye

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the environment variable to non-interactive mode for automated installations
ENV DEBIAN_FRONTEND=noninteractive

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc tzdata net-tools iputils-ping curl ca-certificates \
  && apt-get clean

# Download Microsoft RSA Root Certificate 2017
RUN curl -o /usr/local/share/ca-certificates/microsoft_root_2017.crt https://www.microsoft.com/pkiops/certs/Microsoft%20RSA%20Root%20Certificate%20Authority%202017.crt

# Download DigiCert Global Root G2
RUN curl -o /usr/local/share/ca-certificates/digicert_global_root_g2.crt https://www.digicert.com/CACerts/DigiCertGlobalRootG2.crt.pem

# Download DigiCert Global Root CA
RUN curl -o /usr/local/share/ca-certificates/digicert_global_root_ca.crt https://www.digicert.com/CACerts/DigiCertGlobalRootCA.crt.pem

# Update the CA certificates in the container
RUN update-ca-certificates

ENV TZ Africa/Nairobi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# add app
COPY . .

EXPOSE 3100

CMD ["gunicorn", "src.main:app"]