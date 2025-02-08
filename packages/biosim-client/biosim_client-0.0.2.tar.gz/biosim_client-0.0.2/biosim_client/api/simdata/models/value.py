"""
simdata-api

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 1.0.0
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

from pydantic import (
    BaseModel,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    ValidationError,
    field_validator,
)
from typing_extensions import Self

VALUE_ANY_OF_SCHEMAS = ["List[bool]", "List[float]", "List[int]", "List[str]", "bool", "float", "int", "str"]


class Value(BaseModel):
    """
    Value
    """

    # data type: int
    anyof_schema_1_validator: Optional[StrictInt] = None
    # data type: float
    anyof_schema_2_validator: Optional[Union[StrictFloat, StrictInt]] = None
    # data type: str
    anyof_schema_3_validator: Optional[StrictStr] = None
    # data type: bool
    anyof_schema_4_validator: Optional[StrictBool] = None
    # data type: List[str]
    anyof_schema_5_validator: Optional[List[StrictStr]] = None
    # data type: List[int]
    anyof_schema_6_validator: Optional[List[StrictInt]] = None
    # data type: List[float]
    anyof_schema_7_validator: Optional[List[Union[StrictFloat, StrictInt]]] = None
    # data type: List[bool]
    anyof_schema_8_validator: Optional[List[StrictBool]] = None
    if TYPE_CHECKING:
        actual_instance: Optional[Union[List[bool], List[float], List[int], List[str], bool, float, int, str]] = None
    else:
        actual_instance: Any = None
    any_of_schemas: Set[str] = {"List[bool]", "List[float]", "List[int]", "List[str]", "bool", "float", "int", "str"}

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_anyof(cls, v):
        instance = Value.model_construct()
        error_messages = []
        # validate data type: int
        try:
            instance.anyof_schema_1_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: float
        try:
            instance.anyof_schema_2_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: str
        try:
            instance.anyof_schema_3_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: bool
        try:
            instance.anyof_schema_4_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: List[str]
        try:
            instance.anyof_schema_5_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: List[int]
        try:
            instance.anyof_schema_6_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: List[float]
        try:
            instance.anyof_schema_7_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: List[bool]
        try:
            instance.anyof_schema_8_validator = v
            return v
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        if error_messages:
            # no match
            raise ValueError(
                "No match found when setting the actual_instance in Value with anyOf schemas: List[bool], List[float], List[int], List[str], bool, float, int, str. Details: "
                + ", ".join(error_messages)
            )
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        # deserialize data into int
        try:
            # validation
            instance.anyof_schema_1_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_1_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into float
        try:
            # validation
            instance.anyof_schema_2_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_2_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into str
        try:
            # validation
            instance.anyof_schema_3_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_3_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into bool
        try:
            # validation
            instance.anyof_schema_4_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_4_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[str]
        try:
            # validation
            instance.anyof_schema_5_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_5_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[int]
        try:
            # validation
            instance.anyof_schema_6_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_6_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[float]
        try:
            # validation
            instance.anyof_schema_7_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_7_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[bool]
        try:
            # validation
            instance.anyof_schema_8_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.anyof_schema_8_validator
            return instance
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into Value with anyOf schemas: List[bool], List[float], List[int], List[str], bool, float, int, str. Details: "
                + ", ".join(error_messages)
            )
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(
        self,
    ) -> Optional[Union[Dict[str, Any], List[bool], List[float], List[int], List[str], bool, float, int, str]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())
