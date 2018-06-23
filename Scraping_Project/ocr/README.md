## About

A light container wrapping the [Tesseract](https://github.com/tesseract-ocr/tesseract)
OCR software and pdftotext. The main script is pulled from
[here](https://diging.atlassian.net/wiki/spaces/DCH/pages/5275668/Tutorial+Text+Extraction+and+OCR+with+Tesseract+and+ImageMagick). The container mounts two volumes: one that contains PDFs and a second for the text output.

## Build and Run

```
docker build -t ocr .
docker run -v /path/to/pdfs:/data -v /path/to/text:/text ocr /data /text/
```

The above command builds the Docker container according to the `Dockerfile`. The command breaks down as follows:

* `docker run`: Runs the code...
* `-v /path/to/pdfs:/data`: Mounts the volume containing the PDFs to a directory within the container named `data`
* `-v /path/to/text:/text`: Mounts a volume on the host to which the OCR'd text will be written. The container directory is named `text`.
* `ocr /data /text/`: Runs the `ocr` container built in the build step with the arguments `/data` (the directory containing the PDFs to extract) and `/text/` (the directory to which the extracted text will be written.
