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

import capa.features.extractors.binja.find_binja_api as find_binja_api


def make_binja_python_path(tmp_path):
    python_path = tmp_path / "Binary Ninja.app" / "Contents" / "Resources" / "python"
    module_path = python_path / "binaryninja"
    module_path.mkdir(parents=True)
    (module_path / "__init__.py").write_text("")
    return python_path


def test_validate_binaryninja_path_accepts_install_root(tmp_path):
    python_path = make_binja_python_path(tmp_path)
    install_root = python_path.parent

    assert find_binja_api.validate_binaryninja_path(install_root)
    assert find_binja_api.get_binaryninja_module_path(install_root) == python_path


def test_validate_binaryninja_path_accepts_python_module_path(tmp_path):
    python_path = make_binja_python_path(tmp_path)

    assert find_binja_api.validate_binaryninja_path(python_path)
    assert find_binja_api.get_binaryninja_module_path(python_path) == python_path


def test_find_binaryninja_uses_subprocess_python_module_path(tmp_path, monkeypatch):
    python_path = make_binja_python_path(tmp_path)

    monkeypatch.setattr(find_binja_api, "find_binaryninja_path_via_subprocess", lambda: python_path)

    assert find_binja_api.find_binaryninja() == python_path


def test_find_binaryninja_checks_macos_default_paths(tmp_path, monkeypatch):
    python_path = make_binja_python_path(tmp_path)

    monkeypatch.setattr(find_binja_api, "find_binaryninja_path_via_subprocess", lambda: None)
    monkeypatch.setattr(find_binja_api, "get_default_binaryninja_paths", lambda: [python_path.parent])
    monkeypatch.setattr(find_binja_api.sys, "platform", "darwin")

    assert find_binja_api.find_binaryninja() == python_path
