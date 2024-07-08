FROM python:3.10-slim

# Define o diretório de trabalho dentro do contêiner
COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENTRYPOINT ["streamlit", "run"]

CMD ["Infos.py"]