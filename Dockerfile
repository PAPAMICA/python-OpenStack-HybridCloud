FROM python:3.9

WORKDIR /app
RUN apt install -y jq
RUN git clone https://github.com/PAPAMICA/python-OpenStack-HybridCloud /app
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r /app/requirements.txt

CMD ["python3", "-u", "/app/dashboard.py"]
