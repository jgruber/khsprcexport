FROM python:3

WORKDIR /

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y git pdftk

RUN mkdir /data && \
    mkdir /output && \
    cd /var/lib && \
    git clone https://github.com/jgruber/khsprcexport && \
    cd /var/lib/khsprcexport && \
    pip3 install -r requirements.txt;

VOLUME [ "/data", "/output" ]

ENTRYPOINT [ "/var/lib/khsprcexport/create_publisher_record_cards.py", "--khsdatadir=/data", "--outputdir=/output", "--pdf" ]