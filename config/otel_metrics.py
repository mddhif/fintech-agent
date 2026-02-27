from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader, start_http_server
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry import metrics


resource = Resource(attributes={"service.name":"fintech-agent-service"})
reader = PrometheusMetricReader()

provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)

requests_counter = meter.create_counter(
    name="fintech_requests_total",
    description="total fintech requests"
)

start_http_server(port=9464, addr="0.0.0.0")