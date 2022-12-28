FROM python:3.10.6
EXPOSE 5000
COPY . .
WORKDIR /api
ENV mysql_user="admin"
ENV db_name="companydb"
ENV mysql_new_pwd="CaraFuca2008"
ENV end_point="company.c3hqda7obrsd.us-east-1.rds.amazonaws.com"
RUN pip install -r /api/requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]


#docker build -t challenge-rest-api .
#docker run -p 5000:5000 challenge-rest-api
