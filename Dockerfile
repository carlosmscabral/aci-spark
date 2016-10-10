FROM dockercisco/acitoolkit
RUN git clone https://github.com/carlosmscabral/aci-spark
WORKDIR aci-spark
CMD ["./run.py"]
