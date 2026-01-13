FROM mcr.microsoft.com/devcontainers/python:3.11

# Install bioinformatics tools
RUN apt-get update && apt-get install -y \
    fastqc \
    bwa \
    samtools \
    gatk \
    hisat2 \
    && rm -rf /var/lib/apt/lists/*