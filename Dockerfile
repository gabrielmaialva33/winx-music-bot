FROM python:3.13-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip

CMD python3 -m WinxMusic