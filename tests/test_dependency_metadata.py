# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import tomllib
from pathlib import Path


REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9_.-]+)")


def normalize_package_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def get_requirement_name(requirement: str) -> str:
    requirement = requirement.split(";", 1)[0]
    match = REQUIREMENT_NAME.match(requirement)
    assert match is not None
    return normalize_package_name(match.group(1))


def test_runtime_dependencies_are_pinned_in_requirements():
    project_root = Path(__file__).resolve().parent.parent
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    runtime_dependencies = {
        get_requirement_name(requirement)
        for requirement in pyproject["project"]["dependencies"]
    }
    pinned_dependencies = {
        get_requirement_name(requirement)
        for requirement in (project_root / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if requirement and not requirement.startswith("#")
    }

    assert runtime_dependencies <= pinned_dependencies
