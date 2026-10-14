FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ openjdk-17-jdk-headless python3 python3-numpy python3-numba \
    libboost-all-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
