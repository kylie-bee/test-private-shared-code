import os
import json
from pathlib import Path

from robocorp import workitems, storage, log, vault
from robocorp.tasks import get_output_dir, task


### SETUP ###

PROJECT_ROOT = Path(__file__).parent.parent
ROBOT_ROOT = Path(os.getenv("ROBOT_ROOT", None))
if ROBOT_ROOT is not None:
    PROJECT_ROOT = Path(ROBOT_ROOT)
ARTIFACTS_DIR = Path(os.getenv("ROBOT_ARTIFACTS", None))
if ARTIFACTS_DIR is None:
    ARTIFACTS_DIR = PROJECT_ROOT / "output"
DEVDATA = PROJECT_ROOT / "devdata"


class BotError(Exception):
    """General bot exception.

    TYPE: Unset
    CODE: BASE_ERROR
    """

    CODE = "BASE_ERROR"

    def __init__(self, message: str | None = None):
        super().__init__(message, self.CODE)


class BotApplicationError(BotError, workitems.ApplicationException):
    """Raised when the bot application encounters an error.

    TYPE: Application
    CODE: BOT_APPLICATION_ERROR
    """

    CODE = "BOT_APPLICATION_ERROR"


class BotBusinessError(BotError, workitems.BusinessException):
    """Raised when the bot encounters an error in the business logic.

    TYPE: Business
    CODE: BOT_BUSINESS_ERROR
    """

    CODE = "BOT_BUSINESS_ERROR"


def setup_log() -> None:
    """Tries to use the LOG_LEVEL text asset or environment variable
    to set the log level. If the value is not valid, the default is
    "info". The environment variable will override the asset value.
    """
    try:
        log_level = storage.get_text("LOG_LEVEL")
    except (storage.AssetNotFound, RuntimeError, KeyError):
        log_level = "info"
    log_level = os.getenv("LOG_LEVEL", log_level)
    try:
        log_level = log.FilterLogLevel(log_level)
    except ValueError:
        log_level = log.FilterLogLevel.INFO
    log.setup_log(output_log_level=log_level)


def get_secret(system: str) -> vault.SecretContainer:
    """Gets the appropriate secret from the vault based on
    the system name and the mapping within the Control Room
    asset storage. This is a simple example of how you can
    use the asset storage system to configure your bots.

    In this example, the mapping should be stored in the asset storage
    as a JSON object named "system_credential_index" with the following
    structure:
        {
            "system_name": "secret_name",
            ...
        }

    For the sake of this example, this function loads a mapping from
    a file named "system_credential_index.json" in the devdata directory,
    but if you are using the Control Room, you can create this asset
    in your Workspace and it will use that instead.
    """
    try:
        mapping = storage.get_json("system_credential_index")
    except (storage.AssetNotFound, RuntimeError, KeyError):
        # If the asset is not found, use the local file instead.
        with (DEVDATA / "system_credential_index.json").open() as file:
            mapping = json.load(file)
    try:
        assert isinstance(mapping, dict)
        secret_name = mapping[system]
    except KeyError:
        raise KeyError(f"System {system} not found in mapping.")
    except (TypeError, AssertionError):
        raise TypeError("Mapping is not a dictionary-like JSON object.")
    assert isinstance(secret_name, str)
    return vault.get_secret(secret_name)


__all__ = [
    "BotError",
    "BotApplicationError",
    "BotBusinessError",
    "setup_log",
    "get_secret",
    "PROJECT_ROOT",
    "ROBOT_ROOT",
    "ARTIFACTS_DIR",
    "DEVDATA",
]
