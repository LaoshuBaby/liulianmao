def url_reader(url: str) -> str:
    import requests

    response = requests.get(
        url=url, headers={"User-Agent": "liulianmao_url_reader/0.0.1"}
    )
    content = response.text
    return content
