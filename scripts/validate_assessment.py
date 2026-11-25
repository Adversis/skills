"""Check an assessment record and its references. Requires jsonschema and PyYAML."""

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/threat-model/scripts"))
from validate_register import RegisterLoader, validate as validate_register


def unique_fields(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"Repeated JSON field {name!r}")
        result[name] = value
    return result


def validate_assessment(record, register=None):
    schema = json.loads((ROOT / "schemas/assessment.schema.json").read_text(encoding="utf-8"))
    for error in Draft7Validator(schema).iter_errors(record):
        path = "/".join(map(str, error.absolute_path))
        raise ValueError(f"{path or 'assessment'}: {error.message}")

    affected = set(record["affected_requirements"])
    cited = {case.split("/")[0] for case in record["checks"]}
    for finding in record["findings"]:
        cited.update(finding["requirement_ids"])
    if cited - affected:
        raise ValueError(f"IDs missing from affected_requirements: {sorted(cited - affected)}")
    for case, check in record["checks"].items():
        if check["run"] and check["run"]["revision"] != record["revision"]:
            raise ValueError(f"{case}: run revision differs from the assessed revision")

    if register is not None:
        validate_register(register)
        if register["system"]["name"] != record["system"]:
            raise ValueError("The register and assessment name different systems")
        requirements = {item["id"]: item for item in register["requirements"]}
        if affected - requirements.keys():
            raise ValueError(f"Unknown requirement IDs: {sorted(affected - requirements.keys())}")
        cases = {
            f"{req_id}/{case['id']}"
            for req_id in affected
            for case in requirements[req_id]["verification"]
        }
        unknown = record["checks"].keys() - cases
        if unknown:
            raise ValueError(f"Unknown verification cases: {sorted(unknown)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--register", type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.assessment.read_text(encoding="utf-8"), object_pairs_hook=unique_fields)
        register = None
        if args.register:
            register = yaml.load(args.register.read_text(encoding="utf-8"), Loader=RegisterLoader)
            if register is None:
                raise ValueError("The supplied register is empty")
        validate_assessment(record, register)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"{args.assessment}: {error}", file=sys.stderr)
        return 1
    print(f"Valid assessment: {args.assessment}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
