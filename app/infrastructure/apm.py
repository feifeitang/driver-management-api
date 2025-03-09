from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import FastAPI
import os

apm = make_apm_client(
    {
        "SERVICE_NAME": os.getenv("ELASTIC_APM_SERVICE_NAME", "driver-management-app"),
        "SERVER_URL": os.getenv("ELASTIC_APM_SERVER_URL", "http://apm-server:8200"),
        "ENABLED": True,
    }
)


def init_apm(app: FastAPI):
    """Initialize Elastic APM"""
    app.add_middleware(ElasticAPM, client=apm)
