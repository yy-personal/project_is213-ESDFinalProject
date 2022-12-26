FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./place_an_order.py .
EXPOSE  5030
CMD [ "python", "./place_an_order.py" ]


