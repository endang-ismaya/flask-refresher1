FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY ./packages.txt packages.txt
RUN pip install -r packages.txt --no-cache-dir --upgrade
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]