FROM python:3.11-bullseye as base

# python
ENV PYTHONUNBUFFERED=1

    # make poetry install to this location
ENV POETRY_HOME="/opt/poetry" \
    # make poetry create `.venv` in the project's root
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    VIRTUALENVS_OPTIONS_NO_PIP=true \
    VIRTUALENVS_OPTIONS_NO_SETUP_TOOLS=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

ARG dependencies="curl qt6-base-dev"

# update image os
RUN echo 'deb http://deb.debian.org/debian bullseye-backports main' > /etc/apt/sources.list.d/backports.list && \
    apt-get update && \
    apt-get --assume-yes install apt-utils && \
    apt-get --assume-yes dist-upgrade --no-install-recommends && \
    apt-get --assume-yes install ${dependencies} && \
    apt-get --assume-yes clean && \
    apt-get --assume-yes autoremove && \
    rm --recursive --force /var/lib/apt/lists/*

# create new user:group
ARG user=pi
ARG group=pi
ARG groups=0,dialout

RUN groupadd --gid 1000 ${user} && \
    useradd --gid ${group} --groups ${groups} ${user}


FROM base as installer

RUN curl -sSL https://install.python-poetry.org | python3 -

FROM installer as builder

WORKDIR /build/
COPY . .
RUN poetry install

FROM base as runner

# RUN echo 'deb http://deb.debian.org/debian bullseye-backports main' > /etc/apt/sources.list.d/backports.list && \
#     apt-get update && \
#     apt-get --assume-yes install \
#     qt6-base-dev \
#     libx11-xcb-dev \
#     libxcb1-dev

# create image directory and make active
WORKDIR /app/

COPY --from=installer $POETRY_HOME $POETRY_HOME
COPY --from=builder /build ./

# change active user
USER ${user}

# run programme
ENTRYPOINT ["poetry", "run"]
CMD ["app"]
