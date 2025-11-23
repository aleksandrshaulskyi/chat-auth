from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

from fastapi import FastAPI

from settings import settings


def setup_metrics(application: FastAPI) -> None:
    """
    Setup opentelemtery metrics.
    """
    exporter = OTLPMetricExporter(
        endpoint=settings.opentelemetry_collector_url,
        insecure=True,
    )

    metrics_reader = PeriodicExportingMetricReader(
        exporter=exporter,
        export_interval_millis=1000,
    )

    provider = MeterProvider(
        metric_readers=[metrics_reader],
        resource=Resource.create({'service_name': 'chat_authentication'})
    )

    metrics.set_meter_provider(provider)

    FastAPIInstrumentor.instrument_app(application)
