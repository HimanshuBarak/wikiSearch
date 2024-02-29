FROM python:3.10-slim AS builder

# build stage
RUN apt-get update && apt-get install build-essential -y
RUN pip install -U pip setuptools wheel pip pdm

# copy files
COPY pyproject.toml pdm.lock /project/


WORKDIR /project
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable
RUN pdm list 

# Run stage
FROM python:3.10-slim
WORKDIR /project

RUN apt-get update && apt-get install -y poppler-utils
ENV PYTHONPATH=/project/pkgs

# copy packages from the build stage
COPY --from=builder /project/__pypackages__/3.10/lib /project/pkgs
#copy the source code 
COPY src/ /project/src


# execution command t
CMD ["python","-m","gunicorn","--bind 0.0.0.0:52207","src.app.app:app","-k","uvicorn.workers.UvicornWorker","--max-requests","40","--timeout","260", "--workers","10"]

