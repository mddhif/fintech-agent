from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import os
from dotenv import load_dotenv

load_dotenv()

OTEL_ENDPOINT = os.environ.get("OTEL_ENDPOINT")


def setup_tracing():
    resource = Resource.create({
        SERVICE_NAME: "fintech-agent-service"
    })

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint=OTEL_ENDPOINT
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

