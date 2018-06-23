FROM ubuntu:16.04

ADD . /src

RUN apt update && apt install -y poppler-utils \
                                 tesseract-ocr \
                                 libtesseract-dev

RUN chmod +x /src/extract_text.sh
ENTRYPOINT ["/src/extract_text.sh"]
CMD []
