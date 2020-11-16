from os import path
from kubernetes import client, config

import yaml

config.load_kube_config()


def load_yaml(config_file):
    with open(path.join(path.dirname(__file__), "config/" + config_file)) as f:
        dep = yaml.safe_load(f)

    return dep


def create_deployment(config_file):
    # Create deployment
    dep = load_yaml(config_file)
    mk_apps = client.AppsV1Api()
    resp = mk_apps.create_namespaced_deployment(
        body=dep, namespace="default")
    print("Deployment created. status='%s'" % resp.metadata.name)


def remove_deployment(name):
    # Delete deployment
    mk_apps = client.AppsV1Api()
    resp = mk_apps.delete_namespaced_deployment(
        name=name, namespace="default", body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(resp.status))


def create_job(config_file):
    dep = load_yaml(config_file)
    mk_apps = client.BatchV1Api()
    resp = mk_apps.create_namespaced_job(
        body=dep, namespace="default")
    print("Job created. status='%s'" % str(resp.status))


def remove_job(name):
    mk_apps = client.BatchV1Api()
    resp = mk_apps.delete_namespaced_job(
        name=name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Job deleted. status='%s'" % str(resp.status))


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.

    config_name = "rhombus-job-spec.yaml"
    #config_name = "rhombus-application.yaml"

    #create_deployment(config_name)
    #remove_deployment("rhombus-interview")
    #create_job(config_name)
    remove_job("sequential-job")


if __name__ == '__main__':
    main()
