FROM python:3.9.0

ARG work_dir
WORKDIR ${work_dir}

ENV PATH=/root/.local/bin:${PATH}

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Configure poetry
RUN poetry config cache-dir ${work_dir}/venv && \
    poetry config virtualenvs.in-project true
