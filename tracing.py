from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

def setup_tracing():
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")  # Adjust for your backend
    span_processor = BatchSpanProcessor(otlp_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)
    return tracer