from dataclasses import dataclass
import os
import json
import functools


@dataclass
class _ToggleConfig:
    api_key: str

@dataclass
class _TempoConfig:
    api_key: str
    user_id: str

@dataclass
class Config:
    toggl: _ToggleConfig
    tempo: _TempoConfig


@functools.cache
def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    if not os.path.exists(config_path):
        raise Exception("Config file not found")

    with open(config_path) as f:
        config_data = json.load(f)

    return Config(
        tempo=_TempoConfig(
            **config_data["tempo"]
        ),
        toggl=_ToggleConfig(
            **config_data["toggl"]
        )
    )

config = get_config()
