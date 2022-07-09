FROM python:3.9.0

ARG work_dir \
    env development

# Add a path where poetry is installed
ENV PATH=/root/.local/bin:${PATH} \
    ENV=env\
    POETRY_VERSION=1.1.3

WORKDIR ${work_dir}

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Cache dependencies, only reinstall if dependencies are changed. This also makes build faster.
COPY poetry.lock pyproject.toml ${work_dir}

RUN \
    # Container is already isolated so doesn't need virtualenv
    poetry config virtualenvs.create false && \
    # No install development dependencies if $ENV is production
    poetry install $(test "$ENV" == production && echo "--no-dev")

COPY . ${work_dir}