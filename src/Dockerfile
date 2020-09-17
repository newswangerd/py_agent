FROM python:3.8-alpine
WORKDIR /app

# these are mostly requirements for newspaper3k and nltk
# Running pip install newspaper3k==0.2.8 nltk==3.5 here before requirements.txt
# because these packages take FOREVER to install and I don't want to have to build
# them each time.
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
    && pip install newspaper3k==0.2.8 nltk==3.5

COPY requirements.txt /app
RUN pip install -r requirements.txt 

COPY . /app
RUN pip install -e .

CMD [ "python", "./py_agent/main.py" ]