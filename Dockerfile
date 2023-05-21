FROM python:3.11-alpine as base

ARG ENVIRONMENT

ENV PYROOT /pyroot
ENV PYTHONUSERBASE ${PYROOT}
ENV PATH = ${PATH}:${PYROOT}/bin

RUN if [ "$ENVIRONMENT" = "test" ]; then apk add build-base; fi

RUN PIP_USER=1 pip install pipenv
COPY Pipfile* ./
RUN if [ "$ENVIRONMENT" = "test" ]; then PIP_USER=1 pipenv install --system --deploy --ignore-pipfile --dev; \
    else PIP_USER=1 pipenv install --system --deploy --ignore-pipfile; fi


FROM python:3.7-alpine

ENV PYROOT /pyroot
ENV PYTHONUSERBASE ${PYROOT}
ENV PATH = ${PATH}:${PYROOT}/bin

RUN addgroup -S myapp && adduser -S -G myapp user -u 1234
COPY --chown=user:myapp --from=base ${PYROOT}/ ${PYROOT}/

RUN mkdir -p /usr/src/app/app
WORKDIR /usr/src
COPY --chown=user:myapp app ./app

USER user

 CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]