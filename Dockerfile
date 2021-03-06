ARG PYTHON3_VERSION

FROM python:${PYTHON3_VERSION}

WORKDIR /opt/messy

COPY messy/ messy/
COPY scripts/ scripts/
COPY tests/ tests/
COPY README.md .
COPY setup.py .
COPY setup.cfg .

RUN python3 -m pip install -e .

ENTRYPOINT ["messy"]
