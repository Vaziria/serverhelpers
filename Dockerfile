FROM python:3
COPY . /app
WORKDIR /app

RUN touch environtment/.env
RUN mkdir logs
RUN mkdir category_cache

RUN rm -f category.cache
RUN pip install -r requirements.txt
CMD python ./ingest_toko.py