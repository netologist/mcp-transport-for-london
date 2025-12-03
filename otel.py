import os
import logfire

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:5173/api/v1/private/otel"
_ = logfire.configure(send_to_logfire=False, service_name="ai-lsp")

logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)
