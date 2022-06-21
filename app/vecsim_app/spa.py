import os
from typing import Tuple

from fastapi.staticfiles import StaticFiles


class SinglePageApplication(StaticFiles):
    """Configure a FastAPI application to both serve static files mounted
    at a specific directory and also serve a number of routers for a backend
    API at the same time.
    """

    def __init__(self, directory: os.PathLike, index="index.html") -> None:
        self.index = index

        # set html=True to resolve the index even when no
        # the base path is passed in
        super().__init__(
            directory=directory, packages=None, html=True, check_dir=True
        )

    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response

    def lookup_path(self, path: str) -> Tuple[str, os.stat_result]:
        results = super().lookup_path(path)
        full_path, stat_result = results

        # if a file cannot be found
        if stat_result is None:
            return super().lookup_path(self.index)

        return (full_path, stat_result)
