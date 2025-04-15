from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.sdk.resources import Resource
import time

def setup_monitoring(service_name):
    """Configura o monitoramento básico para o serviço."""
    
    # Criar o exportador para o Google Cloud Monitoring
    exporter = CloudMonitoringMetricsExporter(
        project_id="bankchurnpredict",
        prefix="churn_prediction_"
    )
    
    # Configurar o leitor de métricas
    reader = PeriodicExportingMetricReader(
        exporter,
        export_interval_millis=60000  # Exportar métricas a cada 60 segundos
    )
    
    # Configurar o provedor de métricas com recurso personalizado
    resource = Resource.create({
        "service.name": service_name,
        "service.namespace": "churn_prediction",
        "service.instance.id": "instance-001"
    })
    
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    metrics.set_meter_provider(provider)
    
    # Criar medidor para métricas personalizadas
    meter = metrics.get_meter(__name__)
    
    # Criar contadores e medidores
    request_counter = meter.create_counter(
        name="requests_total",
        description="Número total de requisições",
        unit="1"
    )
    
    latency_histogram = meter.create_histogram(
        name="request_latency",
        description="Latência das requisições",
        unit="ms"
    )
    
    prediction_histogram = meter.create_histogram(
        name="churn_probability",
        description="Distribuição das probabilidades de churn",
        unit="1"
    )
    
    error_counter = meter.create_counter(
        name="errors_total",
        description="Número total de erros",
        unit="1"
    )
    
    return {
        "request_counter": request_counter,
        "latency_histogram": latency_histogram,
        "prediction_histogram": prediction_histogram,
        "error_counter": error_counter
    } 