FROM python:3.12.2-alpine3.19
LABEL maintainer="Javier Llinares - Master en Python"
 
ENV PYTHONUNBUFFERED 1
 
WORKDIR /app
COPY . /app
COPY ./requirements.txt /tmp/requirements.txt
EXPOSE 8000
 
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        kub-user
 
ENV PATH="/py/bin:$PATH"
 
USER kub-user
 
CMD ["uvicorn", "main-model-db:app", "--host", "0.0.0.0", "--port", "8000"]