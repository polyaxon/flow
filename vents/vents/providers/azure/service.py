import os

from typing import TYPE_CHECKING, Optional

from vents.providers.azure.base import (
    get_account_key,
    get_account_name,
    get_connection_string,
)
from vents.providers.base import BaseService

if TYPE_CHECKING:
    from vents.connections.connection import Connection


class AzureService(BaseService):
    account_name: Optional[str]
    account_key: Optional[str]
    connection_string: Optional[str]

    @classmethod
    def load_from_connection(
        cls, connection: Optional["Connection"]
    ) -> Optional["AzureService"]:
        # Check if there are mounting based on secrets/configmaps
        context_paths = []
        if connection:
            if connection.secret and connection.secret.mount_path:
                context_paths.append(connection.secret.mount_path)
            if connection.config_map and connection.config_map.mount_path:
                context_paths.append(connection.config_map.mount_path)
        account_name = get_account_name(context_paths=context_paths)
        account_key = get_account_key(context_paths=context_paths)
        connection_string = get_connection_string(context_paths=context_paths)
        return cls(
            account_name=account_name,
            account_key=account_key,
            connection_string=connection_string,
        )

    def set_env_vars(self):
        if self._account_name:
            os.environ["AZURE_ACCOUNT_NAME"] = self._account_name
        if self._account_key:
            os.environ["AZURE_ACCOUNT_KEY"] = self._account_key
        if self._connection_string:
            os.environ["AZURE_CONNECTION_STRING"] = self._connection_string
