from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Dict

import yaml
from pydantic import BaseModel, Field


class ServiceSettings(BaseModel):
    name: str = Field(..., description="Service name used in the REST endpoint")


class BackendSettings(BaseModel):
    base_url: str = Field(..., description="Backend base URL")
    endpoint_path: str = Field("/", description="Backend path appended to base_url")
    timeout_seconds: int = Field(10, ge=1)
    headers: Dict[str, str] = Field(default_factory=dict)
    mock_enabled: bool = Field(True, description="If true, outbound REST is mocked")


class LoggingSettings(BaseModel):
    level: str = Field("INFO", description="Logging level")


class Settings(BaseModel):
    env: str
    service: ServiceSettings
    backend: BackendSettings
    logging: LoggingSettings


def _settings_path(env: str) -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / f"settings.{env}.yml"


def load_settings() -> Settings:
    env = os.getenv("APP_ENV", os.getenv("ENV", "dev")).lower()
    path = _settings_path(env)
    if not path.exists():
        raise FileNotFoundError(f"Settings file not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Invalid settings file format. Expected a YAML mapping.")

    data["env"] = env
    return Settings(**data)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
