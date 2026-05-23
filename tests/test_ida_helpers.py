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

import sys
import types
import importlib


class IdaStub(types.ModuleType):
    def __getattr__(self, name):
        value = type(name, (), {})
        setattr(self, name, value)
        return value


def import_ida_helpers(monkeypatch, *, loaded=True, segment_end=0x1100):
    calls = []

    idc = IdaStub("idc")
    idc.is_loaded = lambda ea: loaded
    idc.get_segm_end = lambda ea: segment_end

    ida_bytes = IdaStub("ida_bytes")

    def get_bytes(ea, size, gmb_flags=None):
        calls.append((ea, size, gmb_flags))
        return b"A" * size

    ida_bytes.get_bytes = get_bytes

    ida_nalt = IdaStub("ida_nalt")
    ida_nalt.BPU_1B = 1
    ida_nalt.get_default_encoding_idx = lambda bpu: 0

    monkeypatch.setitem(sys.modules, "idc", idc)
    monkeypatch.setitem(sys.modules, "idaapi", IdaStub("idaapi"))
    monkeypatch.setitem(sys.modules, "ida_nalt", ida_nalt)
    monkeypatch.setitem(sys.modules, "idautils", IdaStub("idautils"))
    monkeypatch.setitem(sys.modules, "ida_bytes", ida_bytes)
    monkeypatch.setitem(sys.modules, "ida_funcs", IdaStub("ida_funcs"))
    monkeypatch.setitem(sys.modules, "ida_segment", IdaStub("ida_segment"))
    sys.modules.pop("capa.features.extractors.ida.helpers", None)

    return importlib.import_module("capa.features.extractors.ida.helpers"), calls


def test_read_bytes_at_uses_unpadded_ida_bytes(monkeypatch):
    helpers, calls = import_ida_helpers(monkeypatch)

    assert helpers.read_bytes_at(0x1000, 4) == b"AAAA"
    assert calls == [(0x1000, 4, 0)]


def test_read_bytes_at_truncates_at_segment_end(monkeypatch):
    helpers, calls = import_ida_helpers(monkeypatch, segment_end=0x1002)

    assert helpers.read_bytes_at(0x1000, 4) == b"AA"
    assert calls == [(0x1000, 2, 0)]


def test_read_bytes_at_returns_empty_for_unloaded_address(monkeypatch):
    helpers, calls = import_ida_helpers(monkeypatch, loaded=False)

    assert helpers.read_bytes_at(0x1000, 4) == b""
    assert calls == []
