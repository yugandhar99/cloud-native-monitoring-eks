"""Create a Kubernetes Deployment and Service for the monitoring app.

Before running, set the image value, for example:
export APP_IMAGE=<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/cloud-native-monitoring-eks:latest
"""

import os
from kubernetes import client, config

APP_NAME = os.environ.get("APP_NAME", "cloud-native-monitoring")
APP_IMAGE = os.environ.get("APP_IMAGE", "cloud-native-monitoring:local")
NAMESPACE = os.environ.get("K8S_NAMESPACE", "default")

config.load_kube_config()
api_client = client.ApiClient()

labels = {"app": APP_NAME}

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name=APP_NAME),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels=labels),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels=labels),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="monitoring-app",
                        image=APP_IMAGE,
                        ports=[client.V1ContainerPort(container_port=5000)],
                        readiness_probe=client.V1Probe(
                            http_get=client.V1HTTPGetAction(path="/healthz", port=5000),
                            initial_delay_seconds=10,
                            period_seconds=10,
                        ),
                        liveness_probe=client.V1Probe(
                            http_get=client.V1HTTPGetAction(path="/healthz", port=5000),
                            initial_delay_seconds=15,
                            period_seconds=20,
                        ),
                    )
                ]
            ),
        ),
    ),
)

apps_api = client.AppsV1Api(api_client)
apps_api.create_namespaced_deployment(namespace=NAMESPACE, body=deployment)
print(f"Created deployment: {APP_NAME}")

service = client.V1Service(
    metadata=client.V1ObjectMeta(name=APP_NAME),
    spec=client.V1ServiceSpec(
        selector=labels,
        ports=[client.V1ServicePort(port=80, target_port=5000)],
        type="ClusterIP",
    ),
)

core_api = client.CoreV1Api(api_client)
core_api.create_namespaced_service(namespace=NAMESPACE, body=service)
print(f"Created service: {APP_NAME}")
