FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./shipping_record.py .
CMD [ "python", "./shipping_record.py" ]
