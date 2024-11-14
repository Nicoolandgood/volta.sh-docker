#!/usr/bin/env python3

import http.client, json, subprocess
from urllib.parse import urlparse, urljoin
from pathlib import Path

# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
HTTP_STATUS_TYPES = {
    100: "info",
    200: "success",
    300: "redirection",
    400: "client_error",
    500: "server_error",
}

def get_http_status_type(status_code: int):

    if status_code < 100 or status_code >= 600:
        return None
    
    http_status_code = (status_code // 100) * 100
    return HTTP_STATUS_TYPES.get(http_status_code)

def fetch(
    url: str, 
    method: str = "GET", 
    encoding: str = "utf-8", 
    max_redirection: int = 5,
    headers: dict = {},
) -> dict:

    if max_redirection <= 0:
        raise Exception("Max redirection exceeded.")

    try:
        parsed_url = urlparse(url)
        is_https = parsed_url.scheme == "https"
    
        if is_https:
            connection = http.client.HTTPSConnection(parsed_url.hostname)
        else:
            connection = http.client.HTTPConnection(parsed_url.hostname)
        
        connection.request(method, parsed_url.path or "/", headers=headers)
        
        response = connection.getresponse()

        decoded_data = response.read().decode(encoding)

        status_code = response.status
        status_type = get_http_status_type(status_code)

        if status_type == "redirection":
            location = response.getheader("Location")
            redirection_url = urljoin(url, location)
            max_redirection -= 1
            return fetch(redirection_url, method, encoding, max_redirection, headers)

        return {
            "status_code": response.status,
            "status_type": get_http_status_type(response.status),
            "response": response,
            "data": decoded_data,
        }
    finally:
        connection.close()

PROJECT_DIR = Path(__file__).parent.parent.resolve()

VOLTA_REPO_URL = "https://github.com/volta-cli/volta/releases/latest/"

DOCKER_IMAGE_NAME = "nicoolandgood/volta.sh"

DOCKER_IMAGE_ARCH = [
    "linux/amd64",
    "linux/arm64",
    "linux/arm",
]

INLINE_DOCKER_IMAGE_ARCH = ",".join(DOCKER_IMAGE_ARCH)

if __name__ == "__main__":

    response = fetch(VOLTA_REPO_URL, headers={ "Accept": "application/json" })

    response_type = response.get("status_type")

    if response_type != "success":
        raise Exception("Could not fetch Volta latest release info.")

    response_data = json.loads(response.get("data"))
    tag_name = response_data.get("tag_name")
    version = tag_name[1:]
    
    print(f"Volta latest release found: {tag_name}.")
    
    subprocess.run([
        "docker", 
        "buildx", 
        "build", str(PROJECT_DIR), 
        "--platform", INLINE_DOCKER_IMAGE_ARCH,
        "--tag", f"{DOCKER_IMAGE_NAME}:{version}",
        "--tag", f"{DOCKER_IMAGE_NAME}:latest",
        "--push",
    ])