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

import importlib.util
from pathlib import Path


def load_build_rules_module():
    path = Path(__file__).resolve().parent.parent / "web" / "rules" / "scripts" / "build_rules.py"
    spec = importlib.util.spec_from_file_location("build_rules", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def make_rule(path: Path, name: str, namespace: str):
    path.parent.mkdir(parents=True)
    path.write_text(
        f"""
rule:
  meta:
    name: {name}
    namespace: {namespace}
    scopes:
      static: function
      dynamic: unsupported
    authors:
      - test
  features:
    - number: 1
""",
        encoding="utf-8",
    )


def test_rule_github_link_uses_source_relative_path(tmp_path):
    build_rules = load_build_rules_module()
    rules_dir = tmp_path / "rules"
    rule_path = rules_dir / "lib" / "calculate-modulo-256-via-x86-assembly.yml"
    make_rule(rule_path, "calculate modulo 256 via x86 assembly", "math/arithmetic")

    assert (
        build_rules.get_github_rule_link(rules_dir, rule_path)
        == "https://github.com/mandiant/capa-rules/tree/master/lib/calculate-modulo-256-via-x86-assembly.yml"
    )


def test_render_rule_uses_source_relative_github_link(tmp_path):
    build_rules = load_build_rules_module()
    rules_dir = tmp_path / "rules"
    rule_path = rules_dir / "lib" / "calculate-modulo-256-via-x86-assembly.yml"
    make_rule(rule_path, "calculate modulo 256 via x86 assembly", "math/arithmetic")

    rendered = build_rules.render_rule(
        rules_dir,
        {rule_path.as_posix(): "2026-01-01"},
        rule_path,
    )

    assert "https://github.com/mandiant/capa-rules/tree/master/lib/calculate-modulo-256-via-x86-assembly.yml" in rendered
