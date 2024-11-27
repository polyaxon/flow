import os

from typing import TYPE_CHECKING, Optional

from clipped.utils.json import orjson_dumps

from vents.providers.base import BaseService
from vents.settings import VENTS_CONFIG

if TYPE_CHECKING:
    from vents.connections.connection import Connection


class AnthropicService(BaseService):
    api_key: Optional[str] = None
    is_async: bool = False
    kwargs: Optional[dict] = None

    @classmethod
    def load_from_connection(
        cls, connection: Optional["Connection"]
    ) -> Optional["AnthropicService"]:
        # Check if there are mounting based on secrets/configmaps
        context_paths = []
        if connection:
            if connection.secret and connection.secret.mount_path:
                context_paths.append(connection.secret.mount_path)
            if connection.config_map and connection.config_map.mount_path:
                context_paths.append(connection.config_map.mount_path)

        api_key = VENTS_CONFIG.read_keys(
            context_paths=context_paths, keys=["ANTHROPIC_API_KEY"]
        )
        kwargs = VENTS_CONFIG.read_keys(
            context_paths=context_paths, keys=["ANTHROPIC_KWARGS"]
        )
        return cls(
            api_key=api_key,
            kwargs=kwargs,
        )

    def _set_session(self):
        import anthropic

        kwargs = self.kwargs or {}
        self._session = anthropic.Anthropic(
            api_key=self.api_key,
            **kwargs,
        )

    def set_env_vars(self):
        if self.api_key:
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
        if self.kwargs:
            os.environ["ANTHROPIC_KWARGS"] = orjson_dumps(self.kwargs)
