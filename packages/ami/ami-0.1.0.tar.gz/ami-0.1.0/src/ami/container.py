"""
Module for container-related functionality and detection.
"""

import os

from .envvar import using_envvar


def using_docker_container() -> bool:
    """
    Check specifically if running in a Docker container.

    Returns:
        bool: True if running in a Docker container, False otherwise.
    """
    return os.path.exists("/.dockerenv")


def using_podman_container() -> bool:
    """
    Check specifically if running in a Podman container.

    Returns:
        bool: True if running in a Podman container, False otherwise.
    """
    return os.path.exists("/run/.containerenv")


def using_kubernetes() -> bool:
    """
    Check if running in a Kubernetes pod.

    Returns:
        bool: True if running in a Kubernetes pod, False otherwise.
    """
    return using_envvar("KUBERNETES_SERVICE_HOST")


def using_runpod() -> bool:
    """
    Check if running in a RunPod.io environment.

    Returns:
        bool: True if running in RunPod.io, False otherwise.
    """
    return using_envvar("RUNPOD_POD_ID")


def using_container() -> bool:
    """
    Check if running in any supported container (Docker or Podman).

    Returns:
        bool: True if running in any supported container, False otherwise.
    """
    return using_docker_container() or using_podman_container()
