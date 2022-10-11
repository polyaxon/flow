#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
# This file and its contents are licensed under the AGPLv3 License.
# Please see the included NOTICE for copyright information and
# LICENSE-AGPL for a copy of the license.

import re
import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.serializers.json
import django.core.validators
import django.db.models.deletion
import django.utils.timezone

from django.conf import settings
from django.db import migrations, models

import haupt.common.validation.blacklist


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "db_user",
                "abstract": False,
                "swappable": "AUTH_USER_MODEL",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Artifact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("state", models.UUIDField(db_index=True)),
                ("name", models.CharField(db_index=True, max_length=256)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("analysis", "analysis"),
                            ("artifact", "artifact"),
                            ("audio", "audio"),
                            ("chart", "chart"),
                            ("coderef", "coderef"),
                            ("confusion", "confusion"),
                            ("csv", "csv"),
                            ("curve", "curve"),
                            ("data", "data"),
                            ("dataframe", "dataframe"),
                            ("dir", "dir"),
                            ("docker_image", "docker_image"),
                            ("dockerfile", "dockerfile"),
                            ("env", "env"),
                            ("file", "file"),
                            ("histogram", "histogram"),
                            ("html", "html"),
                            ("image", "image"),
                            ("iteration", "iteration"),
                            ("markdown", "markdown"),
                            ("metric", "metric"),
                            ("model", "model"),
                            ("psv", "psv"),
                            ("ssv", "ssv"),
                            ("system", "system"),
                            ("table", "table"),
                            ("tensor", "tensor"),
                            ("tensorboard", "tensorboard"),
                            ("text", "text"),
                            ("tsv", "tsv"),
                            ("video", "video"),
                        ],
                        db_index=True,
                        max_length=12,
                    ),
                ),
                ("path", models.CharField(blank=True, max_length=256, null=True)),
                ("summary", models.JSONField()),
            ],
            options={
                "db_table": "db_artifact",
            },
        ),
        migrations.CreateModel(
            name="ArtifactLineage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("is_input", models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                "db_table": "db_artifactlineage",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "live_state",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "live"),
                            (0, "archived"),
                            (-1, "deletion_progressing"),
                        ],
                        db_index=True,
                        default=1,
                        null=True,
                    ),
                ),
                (
                    "tags",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("readme", models.TextField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            ),
                            haupt.common.validation.blacklist.validate_blacklist_name,
                        ],
                    ),
                ),
            ],
            options={
                "db_table": "db_project",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "live_state",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "live"),
                            (0, "archived"),
                            (-1, "deletion_progressing"),
                        ],
                        db_index=True,
                        default=1,
                        null=True,
                    ),
                ),
                (
                    "tags",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("readme", models.TextField(blank=True, null=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("wait_time", models.IntegerField(blank=True, null=True)),
                ("duration", models.IntegerField(blank=True, null=True)),
                (
                    "raw_content",
                    models.TextField(
                        blank=True,
                        help_text="The raw yaml content of the polyaxonfile/specification.",
                        null=True,
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True,
                        help_text="The compiled yaml content of the polyaxonfile/specification.",
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("compiled", "compiled"),
                            ("created", "created"),
                            ("done", "done"),
                            ("failed", "failed"),
                            ("on_schedule", "on_schedule"),
                            ("processing", "processing"),
                            ("queued", "queued"),
                            ("resuming", "resuming"),
                            ("retrying", "retrying"),
                            ("running", "running"),
                            ("scheduled", "scheduled"),
                            ("skipped", "skipped"),
                            ("starting", "starting"),
                            ("stopped", "stopped"),
                            ("stopping", "stopping"),
                            ("succeeded", "succeeded"),
                            ("unknown", "unknown"),
                            ("unschedulable", "unschedulable"),
                            ("upstream_failed", "upstream_failed"),
                            ("warning", "warning"),
                        ],
                        db_index=True,
                        default="created",
                        max_length=16,
                        null=True,
                    ),
                ),
                (
                    "status_conditions",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default=None,
                        max_length=128,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^[-a-zA-Z0-9_]+\\Z"),
                                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                                "invalid",
                            )
                        ],
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("builder", "builder"),
                            ("cleaner", "cleaner"),
                            ("dag", "dag"),
                            ("dask", "dask"),
                            ("flink", "flink"),
                            ("job", "job"),
                            ("matrix", "matrix"),
                            ("mpijob", "mpijob"),
                            ("mxjob", "mxjob"),
                            ("notifier", "notifier"),
                            ("pytorchjob", "pytorchjob"),
                            ("ray", "ray"),
                            ("schedule", "schedule"),
                            ("service", "service"),
                            ("spark", "spark"),
                            ("tfjob", "tfjob"),
                            ("tuner", "tuner"),
                            ("watchdog", "watchdog"),
                            ("xgbjob", "xgbjob"),
                        ],
                        db_index=True,
                        max_length=12,
                    ),
                ),
                (
                    "runtime",
                    models.CharField(
                        blank=True, db_index=True, max_length=12, null=True
                    ),
                ),
                (
                    "is_managed",
                    models.BooleanField(
                        default=True,
                        help_text="If this entity is managed by the platform.",
                    ),
                ),
                (
                    "pending",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("approval", "approval"),
                            ("build", "build"),
                            ("cache", "cache"),
                            ("upload", "upload"),
                        ],
                        db_index=True,
                        help_text="If this entity requires approval before it should run.",
                        max_length=8,
                        null=True,
                    ),
                ),
                ("meta_info", models.JSONField(blank=True, default=dict, null=True)),
                ("params", models.JSONField(blank=True, null=True)),
                ("inputs", models.JSONField(blank=True, null=True)),
                ("outputs", models.JSONField(blank=True, null=True)),
                (
                    "cloning_kind",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("cache", "cache"),
                            ("copy", "copy"),
                            ("restart", "restart"),
                        ],
                        max_length=12,
                        null=True,
                    ),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        blank=True,
                        related_name="runs",
                        through="db.ArtifactLineage",
                        to="db.artifact",
                    ),
                ),
                (
                    "original",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="clones",
                        to="db.run",
                    ),
                ),
                (
                    "pipeline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pipeline_runs",
                        to="db.run",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="runs",
                        to="db.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "db_run",
                "abstract": False,
            },
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(fields=["name"], name="db_project_name_4bfc0e_idx"),
        ),
        migrations.AddField(
            model_name="artifactlineage",
            name="artifact",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs_lineage",
                to="db.artifact",
            ),
        ),
        migrations.AddField(
            model_name="artifactlineage",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="artifacts_lineage",
                to="db.run",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="artifact",
            unique_together={("name", "state")},
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddIndex(
            model_name="run",
            index=models.Index(fields=["name"], name="db_run_name_47fc7c_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="artifactlineage",
            unique_together={("run", "artifact", "is_input")},
        ),
    ]