#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.
from datetime import datetime
from typing import List

import ujson

from rest_framework import status

from django.http import HttpResponse

from asgiref.sync import sync_to_async
from polyaxon import settings
from polyaxon.fs.async_manager import (
    delete_file_or_dir,
    download_dir,
    open_file,
    upload_data,
)
from polyaxon.fs.types import FSSystem
from polyaxon.utils.path_utils import delete_path
from traceml.logging import V1Log, V1Logs


async def clean_tmp_logs(fs: FSSystem, run_uuid: str):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HttpResponse(
            detail="Run's logs was not collected, resource was not found.",
            status=status.HTTP_400_BAD_REQUEST,
        )
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    await delete_file_or_dir(fs=fs, subpath=subpath, is_file=False)


async def upload_logs(fs: FSSystem, run_uuid: str, logs: List[V1Log]):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HttpResponse(
            detail="Run's logs was not collected, resource was not found.",
            status=status.HTTP_400_BAD_REQUEST,
        )
    for c_logs in V1Logs.chunk_logs(logs):
        last_file = datetime.timestamp(c_logs.logs[-1].timestamp)
        if settings.AGENT_CONFIG.compressed_logs:
            subpath = "{}/plxlogs/{}.plx".format(run_uuid, last_file)
            await upload_data(
                fs=fs,
                subpath=subpath,
                data="{}\n{}".format(c_logs.get_csv_header(), c_logs.to_csv()),
            )
        else:
            subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
            await upload_data(fs=fs, subpath=subpath, data=c_logs.to_dict(dump=True))


async def content_to_logs(content, logs_path):
    if not content:
        return []

    @sync_to_async
    def convert():
        # Version handling
        if ".plx" in logs_path:
            return V1Logs.read_csv(content).logs
        # Legacy logs
        return ujson.loads(content).get("logs", [])

    return await convert()


async def download_logs_file(
    fs: FSSystem, run_uuid: str, last_file: str, check_cache: bool = True
) -> (str, str):
    subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
    content = await open_file(fs=fs, subpath=subpath, check_cache=check_cache)

    return await content_to_logs(content, subpath)


async def download_tmp_logs(fs: FSSystem, run_uuid: str) -> str:
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    return await download_dir(fs=fs, subpath=subpath)