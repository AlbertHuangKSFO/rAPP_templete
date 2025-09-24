"""
This module provides a Prometheus Metrics Registry with counters.
"""

from prometheus_client import (
    CollectorRegistry,
    Counter,
    disable_created_metrics,
    generate_latest,
)
from .config import get_config
from .mtls_logging import logger

SERVICE_PREFIX = get_config()["container_name"].replace("-", "_")


def _create_metrics() -> dict[str, Counter]:
    return {
        "network_configuration_successful_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="network_configuration_successful_requests",
            documentation="Total number of successful Network Configuration requests",
        ),
        "network_configuration_failed_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="network_configuration_failed_requests",
            documentation="Total number of failed Network Configuration requests",
        ),
        "topology_successful_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="topology_successful_requests",
            documentation="Total number of successful Topology & Inventory requests",
        ),
        "topology_failed_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="topology_failed_requests",
            documentation="Total number of failed Topology & Inventory requests",
        ),
        "messages_consumed": Counter(
            namespace=SERVICE_PREFIX,
            name="messages_consumed",
            documentation="Total number of messages consumed from Message Bus",
        ),
        "filtered_messages_by_motype": Counter(
            namespace=SERVICE_PREFIX,
            name="filtered_messages_by_motype",
            documentation="Number of messages that have been filtered by MO Type",
        ),
        "filtered_messages_by_fdn": Counter(
            namespace=SERVICE_PREFIX,
            name="filtered_messages_by_fdn",
            documentation="Number of messages that are relevant to the cells collected at startup",
        ),
        "complete_batch_of_messages_consumed": Counter(
            namespace=SERVICE_PREFIX,
            name="complete_batch_of_messages_consumed",
            documentation="Total number of complete batches consumed",
        ),
        "partial_batch_of_messages_consumed": Counter(
            namespace=SERVICE_PREFIX,
            name="partial_batch_of_messages_consumed",
            documentation="Total number of batches which have reached timeout that are partially filled",
        ),
        "empty_batch_of_messages_consumed": Counter(
            namespace=SERVICE_PREFIX,
            name="empty_batch_of_messages_consumed",
            documentation="Total number of batches which have reached timeout with zero messages",
        ),
        "schema_registry_successful_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="schema_registry_successful_requests",
            documentation="Total number of successful requests made to Schema Registry",
        ),
        "schema_registry_failed_requests": Counter(
            namespace=SERVICE_PREFIX,
            name="schema_registry_failed_requests",
            documentation="Total number of failed requests made to Schema Registry",
        ),
    }


class MetricsRegistry(CollectorRegistry):
    """
    Implementation of Prometheus Client's CollectorRegistry.
    """

    def __init__(self):
        super().__init__()
        disable_created_metrics()
        self.counters = _create_metrics()
        self._register_counters()

    def _register_counters(self) -> None:
        for counter in self.counters.values():
            self.register(counter)
        logger.debug(
            f"Created metrics registry in format:\n{generate_latest(self).decode('utf-8')}"
        )

    def _unregister_counters(self) -> None:
        for counter in self.counters.values():
            self.unregister(counter)
        self.counters = {}


metrics_registry = MetricsRegistry()
