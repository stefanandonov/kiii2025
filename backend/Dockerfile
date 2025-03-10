FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
#ENV DB_HOST=${DB_HOST}
#RUN echo $DB_HOST
CMD ["python", "app.py"]