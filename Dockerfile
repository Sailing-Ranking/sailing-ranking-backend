# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

WORKDIR /app
RUN pip install --no-cache-dir pipenv
COPY . .

ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv sync

EXPOSE 8080

# run main.py
CMD ["pipenv", "run", "python", "main.py"]
