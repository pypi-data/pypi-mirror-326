"""
biosim-server

No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The version of the OpenAPI document: 0.0.1
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict
from typing_extensions import Self

from biosim_client.api.biosim.models.comparison_statistics import ComparisonStatistics
from biosim_client.api.biosim.models.run_data import RunData
from biosim_client.api.biosim.models.simulation_run_info import SimulationRunInfo


class GenerateStatisticsOutput(BaseModel):
    """
    GenerateStatisticsOutput
    """

    sims_run_info: List[SimulationRunInfo]
    comparison_statistics: Dict[str, List[List[ComparisonStatistics]]]
    sim_run_data: Optional[List[RunData]] = None
    __properties: ClassVar[List[str]] = ["sims_run_info", "comparison_statistics", "sim_run_data"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GenerateStatisticsOutput from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in sims_run_info (list)
        _items = []
        if self.sims_run_info:
            for _item_sims_run_info in self.sims_run_info:
                if _item_sims_run_info:
                    _items.append(_item_sims_run_info.to_dict())
            _dict["sims_run_info"] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in comparison_statistics (dict of array)
        _field_dict_of_array = {}
        if self.comparison_statistics:
            for _key_comparison_statistics in self.comparison_statistics:
                if self.comparison_statistics[_key_comparison_statistics] is not None:
                    _field_dict_of_array[_key_comparison_statistics] = [
                        _item.to_dict() for _item in self.comparison_statistics[_key_comparison_statistics]
                    ]
            _dict["comparison_statistics"] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of each item in sim_run_data (list)
        _items = []
        if self.sim_run_data:
            for _item_sim_run_data in self.sim_run_data:
                if _item_sim_run_data:
                    _items.append(_item_sim_run_data.to_dict())
            _dict["sim_run_data"] = _items
        # set to None if sim_run_data (nullable) is None
        # and model_fields_set contains the field
        if self.sim_run_data is None and "sim_run_data" in self.model_fields_set:
            _dict["sim_run_data"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GenerateStatisticsOutput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "sims_run_info": [SimulationRunInfo.from_dict(_item) for _item in obj["sims_run_info"]]
            if obj.get("sims_run_info") is not None
            else None,
            "comparison_statistics": obj.get("comparison_statistics"),
            "sim_run_data": [RunData.from_dict(_item) for _item in obj["sim_run_data"]]
            if obj.get("sim_run_data") is not None
            else None,
        })
        return _obj
