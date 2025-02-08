# -*- coding: utf-8 -*-
from typing import Optional, Union

from enum import Enum
import json
from warnings import deprecated

from .vfg_0_4_0 import VFG, Tensor
from .vfg_0_2_0 import migrate as migrate_from_0_2_0


class ValidationError(Exception, Enum):
    """
    The types of validation error that can result from a VFG.
    """

    InvalidVariableName = "Invalid variable name"
    InvalidVariableItemCount = "Invalid variable item count"
    MissingVariable = "Missing variable"
    MissingProbability = "Missing probability"
    VariableMissingInVariableList = "Variable missing in variable list"
    IncorrectProbabilityLength = "Incorrect probability length"
    InvalidShapeError = "Invalid shape error"


JsonSerializationError = ValidationError


# Define a global variable
store: Optional[VFG] = None


@deprecated("Use pydantic json schema creation instead")
def vfg_to_json_schema(indent: int = 2) -> tuple[dict, str]:
    vfg_schema_dict: dict = VFG.model_json_schema()
    vfg_schema_json = json.dumps(vfg_schema_dict, indent=indent)
    return vfg_schema_dict, vfg_schema_json


@deprecated(
    "Call vfg_upgrade; this function is redundant and the other method is better named."
)
def vfg_from_json(json_data: Union[dict, str]) -> VFG:
    """
    See vfg_upgrade
    :param json_data: The json data to up-convert
    :return: The VFG data
    """
    return vfg_upgrade(json_data)


def vfg_upgrade(json_data: Union[dict, str]) -> VFG:
    """
    Upgrades the incoming VFG from JSON data to the latest version supported.
    This calls migrate methods to update from earlier versions to the latest version.
    :param json_data: Incoming json data, in either dictionary or string format
    :return: A VFG object, in the latest schema.
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    if not isinstance(json_data, dict):
        raise AttributeError("json_data must be dict or str")

    if json_data["version"] == "0.2.0":
        json_data = migrate_from_0_2_0(json_data)
    return VFG(**json_data)


@deprecated("Use pydantic JSON conversions instead")
def vfg_from_dict(dict_data: dict) -> VFG:
    return VFG(**dict_data)


@deprecated("Use pydantic JSON conversions instead")
def vfg_to_json(vfg: VFG, indent: int = 2) -> str:
    return vfg.model_dump_json(indent=indent)


@deprecated("Rely on gpil-pipline for persistence; pyvfg should be stateless!")
def set_graph(vfg: VFG):
    global store
    store = vfg


@deprecated("Rely on gpil-pipeline for persistence; pyvfg should be stateless!")
def get_graph() -> VFG:
    global store
    return store


def validate(vfg: VFG) -> Optional[ValidationError]:
    """
    Determines if the given VFG, which was valid according to the JSON schema, actually represents
    a processable VFG according to its type.
    :param vfg: The input VFG type
    :return: ValidationError if the VFG is invalid; None on success
    """

    def is_valid_name(var_name: str) -> bool:
        return len(var_name) > 0 and all(
            [c.isalnum() or c == "_" or c == "-" or c == "." for c in var_name]
        )

    # check that all variables have a valid name, and that every variable has at least one element
    if not all([is_valid_name(var_name) for var_name in vfg.variables.keys()]):
        return ValidationError.InvalidVariableName
    if not all([len(values.get_elements()) > 0 for values in vfg.variables.values()]):
        return ValidationError.InvalidVariableItemCount

    # check that all factors have valid variables
    for factor in vfg.factors:
        # basic checks
        if len(factor.variables) == 0:
            return ValidationError.MissingVariable
        if len(factor.values) == 0:
            return ValidationError.MissingProbability
        for variable in factor.variables:
            if variable not in vfg.variables:
                return ValidationError.VariableMissingInVariableList

        # check that the factor's values have the correct length
        for idx, variable in enumerate(factor.variables):
            try:
                if len(_get_rank(factor.values, idx)) != len(
                    vfg.variables[variable].get_elements()
                ):
                    return ValidationError.IncorrectProbabilityLength
            except IndexError:
                return ValidationError.InvalidShapeError

    # this is a success (per the rust code)
    return None


def _get_rank(tensor: Tensor, idx: int) -> Tensor:
    for i in range(idx):
        tensor = tensor.root[0]
    return tensor
