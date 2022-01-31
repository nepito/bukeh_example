FROM python:3.8
RUN pip install bokeh
WORKDIR /myapp
COPY . .
CMD ["make", "run"]