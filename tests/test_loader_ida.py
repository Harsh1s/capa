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

import capa.loader


def test_idalib_open_database_args_load_resources_for_new_inputs(tmp_path):
    sample = tmp_path / "sample.exe"
    sample.write_bytes(b"MZ")

    assert capa.loader.get_idalib_open_database_args(sample).endswith(" -R")


def test_idalib_open_database_args_skip_resources_for_ida_database(tmp_path):
    ida_db = tmp_path / "sample.i64"
    ida_db.write_bytes(b"IDA")

    assert not capa.loader.get_idalib_open_database_args(ida_db).endswith(" -R")


def test_idalib_open_database_args_skip_resources_for_sidecar_database(tmp_path):
    sample = tmp_path / "sample.exe"
    sample.write_bytes(b"MZ")
    sample.with_suffix(".id0").write_bytes(b"IDA")

    assert capa.loader.has_ida_database(sample)
    assert not capa.loader.get_idalib_open_database_args(sample).endswith(" -R")
