#   Copyright 2020 Logical Clocks AB
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from __future__ import annotations

from typing import Any, Dict, List, Optional

import humps


class Inode:
    def __init__(
        self,
        attributes: Dict[str, Any],
        href: Optional[str] = None,
        zip_state: Optional[str] = None,
        tags: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> None:
        self._path = attributes["path"]

    @classmethod
    def from_response_json(cls, json_dict: Dict[str, Any]) -> List[Inode]:
        json_decamelized = humps.decamelize(json_dict)["items"]
        for inode in json_decamelized:
            _ = inode.pop("type", None)
        return [cls(**inode) for inode in json_decamelized]

    @property
    def path(self) -> str:
        return self._path
