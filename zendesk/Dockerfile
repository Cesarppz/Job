FROM  python:3.8.13-bullseye
WORKDIR /app
COPY /app .
RUN pip install -r requirements.txt --no-cache-dir
CMD tail -f /dev/null
#CMD ["python3","main.py","@args.txt"]