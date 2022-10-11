#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.
import logging
import os

import uvicorn

from polyaxon.utils.workers_utils import get_core_workers

_logger = logging.getLogger("haupt.cli")


def start_app(
    app,
    app_name,
    host: str = None,
    port: int = None,
    log_level: str = None,
    workers: int = None,
    per_core: bool = False,
    uds: str = None,
):
    host = host or "0.0.0.0"
    port = int(port or 8000)
    log_level = log_level or "warning"
    if per_core:
        workers = get_core_workers(per_core=workers or 2)
    else:
        workers = workers or get_core_workers(per_core=2)

        _logger.info(
            "{app_name} is running on http://{host}:{port} in process {pid}".format(
                app_name=app_name, host=host, port=port, pid=os.getpid()
            )
        )
    uvicorn.run(
        app,
        host=host,
        port=port,
        access_log=False,
        log_level=log_level.lower(),
        workers=workers,
        uds=uds,
        timeout_keep_alive=120,
    )