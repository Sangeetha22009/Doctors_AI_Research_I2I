FROM python:3.9
WORKDIR /src
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./src /src/app
EXPOSE 9898
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9898"]
