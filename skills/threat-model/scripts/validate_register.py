"""Validate a security requirements register. Requires PyYAML and jsonschema."""

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator


SCHEMA = Path(__file__).resolve().parents[1] / "assets" / "requirements.schema.json"


class RegisterLoader(yaml.SafeLoader):
    """Reject repeated YAML fields before a loader can silently overwrite them."""

    def compose_mapping_node(self, anchor):
        node = super().compose_mapping_node(anchor)
        fields = set()
        for key_node, _ in node.value:
            if key_node.tag not in ("tag:yaml.org,2002:str", "tag:yaml.org,2002:merge"):
                raise yaml.constructor.ConstructorError(
                    "while reading a register", node.start_mark,
                    "expected a string field name", key_node.start_mark,
                )
            field = (key_node.tag, key_node.value)
            if field in fields:
                raise yaml.constructor.ConstructorError(
                    "while reading a register", node.start_mark,
                    f"repeated field {key_node.value!r}", key_node.start_mark,
                )
            fields.add(field)
        return node


def validate(register):
    validator = Draft7Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    for error in validator.iter_errors(register):
        path = "/".join(str(part) for part in error.absolute_path)
        raise ValueError(f"{path or 'register'}: {error.message}")

    requirements = set()
    for item in register["requirements"]:
        requirement_id = item["id"]
        if requirement_id in requirements:
            raise ValueError(f"Duplicate requirement ID {requirement_id}")
        requirements.add(requirement_id)
        cases = set()
        for case in item["verification"]:
            case_id = case["id"]
            if case_id in cases:
                raise ValueError(f"Duplicate verification case {requirement_id}/{case_id}")
            cases.add(case_id)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register", type=Path)
    args = parser.parse_args()
    try:
        with args.register.open(encoding="utf-8") as stream:
            validate(yaml.load(stream, Loader=RegisterLoader))
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"{args.register}: {error}", file=sys.stderr)
        return 1
    print(f"Valid register: {args.register}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
