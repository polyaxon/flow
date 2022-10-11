#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

# isort: skip_file

# Default configs
from haupt.common.celeryp.routes import get_routes
from haupt.common.settings.api import set_api
from haupt.common.settings.assets import set_assets
from haupt.common.settings.celery import set_celery
from haupt.common.settings.cors import set_cors
from haupt.common.settings.logging import set_logging
from haupt.common.settings.admin import set_admin
from haupt.common.settings.middlewares import set_middlewares
from haupt.common.settings.secrets import set_secrets
from haupt.polyconf.config_manager import ROOT_DIR, config

context = locals()
set_logging(
    context=context,
    root_dir=ROOT_DIR,
    log_level=config.log_level,
    log_handlers=config.log_handlers,
    debug=config.is_debug_mode,
)
set_admin(context=context, config=config)
set_secrets(context=context, config=config)
if config.is_streams_service:
    from .streams import set_app
else:
    from .platform import set_app

set_app(context=context, config=config)
set_cors(context=context, config=config)
set_api(context=context, config=config)
set_middlewares(context=context, config=config)
set_assets(context=context, root_dir=ROOT_DIR, config=config)
if config.scheduler_enabled:
    set_celery(context=context, config=config, routes=get_routes())

from haupt.common.settings.defaults import *

# Service configs
from .rest import *