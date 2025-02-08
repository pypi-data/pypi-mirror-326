"""
The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.

    Dev: wh0ami
Licence: Public Domain <https://unlicense.org>
Project: https://codeberg.org/wh0ami/hcloud-rdns-manager
"""

import jsonschema
from loguru import logger


def validate_config(config: dict) -> bool:
    """
    Validate a configuration file by using jsonschema.

    :param config: The config, which should be validated.
    :return: Whether the validation was successful.
    """
    logger.info("Validating passed rdns zone config...")

    # define a schema for the configuration
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["hcloud"],
        "properties": {
            "hcloud": {
                "type": "object",
                "additionalProperties": False,
                "required": ["projects"],
                "properties": {
                    "projects": {
                        "type": "object",
                        "additionalProperties": False,
                        "minProperties": 1,
                        "patternProperties": {
                            "^[a-zA-Z0-9-]+$": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["token", "servers"],
                                "properties": {
                                    "token": {
                                        "type": "string",
                                        "pattern": "^[a-zA-Z0-9]{64}$",
                                    },
                                    "servers": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "minProperties": 1,
                                        "patternProperties": {
                                            "^[0-9]+$": {
                                                "type": "object",
                                                "additionalProperties": False,
                                                "required": ["rdns"],
                                                "properties": {
                                                    "rdns": {
                                                        "type": "object",
                                                        "additionalProperties": False,
                                                        "patternProperties": {
                                                            "^([0-9\\.]+|[0-9a-fA-F:]+)$": {
                                                                "type": "string",
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    # validate the schema, quit on error
    try:
        jsonschema.validate(instance=config, schema=schema)
    except jsonschema.exceptions.ValidationError as error:
        logger.error("The rdns zone config is invalid: " + str(error))
        return False
    except Exception as error:  # noqa: BLE001
        logger.error("Error while validating the rdns zone config: " + str(error))
        return False

    # only on success
    logger.info("The passed rdns zone config is valid!")
    return True
