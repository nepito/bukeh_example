FROM islasgeci/base:latest
RUN pip install \
    black \
    bokeh \
    codecov \
    fastapi \
    flake8 \
    mutmut \
    pandas \
    pylint \
    pytest \
    pytest-cov \
    requests \
    uvicorn
WORKDIR /workdir
COPY . .
RUN make install