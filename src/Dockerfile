FROM python:3.8-alpine
WORKDIR /app


COPY requirements.txt /app

# these are mostly requirements for newspaper3k and nltk
RUN apk add \
        libxml2-dev \
        libxslt-dev \
        libffi-dev \
        gcc \
        musl-dev \
        libgcc \
        openssl-dev \
        curl \
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
    && pip install -r requirements.txt
COPY . /app
RUN pip install -e .

CMD [ "python", "./py_agent/main.py" ]