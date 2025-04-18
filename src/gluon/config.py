"""
Configuration settings and constants
"""

DATA_REPO_PATH = "./__internal__/data_repo"

REPOSITORY_URLS = {
    "flask": "https://github.com/pallets/flask.git",
    "quart": "https://github.com/pallets/quart.git",
    "sanic": "https://github.com/sanic-org/sanic.git",
    "django": "https://github.com/django/django.git",
    "fastapi": "https://github.com/fastapi/fastapi.git",
    "uvicorn": "https://github.com/encode/uvicorn.git",
    "starlette": "https://github.com/encode/starlette.git",
    "pyrmaid": "https://github.com/Pylons/pyramid.git",
    "gunicorn": "https://github.com/benoitc/gunicorn.git",
    "connexion": "https://github.com/spec-first/connexion.git",
    "aiohttp": "https://github.com/aio-libs/aiohttp.git",
}

# framework: [src_path, test_path]
REPOSITORIES = {
    "flask": ["src", "tests"],
    "quart": ["src", "tests"],
    "sanic": ["sanic", "tests"],
}


RETRIEVE_METHODS = {
    "pair": {
        "similarity_search": {
            "k": 5,
        },
        "similarity_search_with_relevance_scores": {
            "k": 5,
        },
        "similarity_search_with_relevance_scores_threshold": {
            "k": 5,
            "score_threshold": 0.65,
        },
        "similarity_search_with_score": {
            "k": 5,
        },
        "mmr": {
            "k": 5,
            "fetch_k": 10, # the number of items to fetch from the database
        },
        "similarity_score_threshold": {
            "k": 5,
            "score_threshold": 0.6,
        },
        "ensemble": {
            "k": 5,
            "bm25_topk": 5,
        },
    },
    "code": {
        "similarity_search": {
            "k": 5,
        },
        "similarity_search_with_relevance_scores": {
            "k": 5,
        },
        "similarity_search_with_relevance_scores_threshold": {
            "k": 5,
            "score_threshold": 0.65,
        },
        "similarity_search_with_score": {
            "k": 5,
        },
        "mmr": {
            "k": 5,
            "fetch_k": 10,
        },
        "similarity_score_threshold": {
            "k": 5,
            "score_threshold": 0.65,
        },
        "ensemble": {
            "k": 5,
            "bm25_topk": 5,
        },
    },
}

