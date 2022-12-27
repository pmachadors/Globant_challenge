FROM python:3.10
EXPOSE 5000
COPY . .
WORKDIR /api
ENV mysql_user=""
ENV db_name=""
ENV mysql_new_pwd=""
ENV end_point=""
RUN pip install -r /api/requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]


#docker build -t challenge-rest-api .
#docker run -p 5000:5000 challenge-rest-api
