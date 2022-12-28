FROM python:3.10
COPY . work
WORKDIR /work/api
ENV mysql_user=""
ENV db_name=""
ENV mysql_new_pwd=""
ENV end_point=""
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]

#docker build -t challenge-rest-api .
#docker run -p 5000:5000 challenge-rest-api
