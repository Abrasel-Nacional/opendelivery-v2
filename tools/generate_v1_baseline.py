#!/usr/bin/env python3
"""Generate internal v1 baseline reference docs from an OpenAPI file.

Usage:
  python tools/generate_v1_baseline.py --input c:/OpenDelivery/opendelivery/openapi.yaml
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ANCHOR_LINK_RE = re.compile(r"\[([^\]]+)\]\(#([^\)]+)\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def clean_text(text: object) -> str:
    s = str(text)
    s = ANCHOR_LINK_RE.sub(r"\1", s)
    s = HTML_TAG_RE.sub("", s)
    s = s.replace("|", "\\|").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def md_escape(text: object | None) -> str:
    if text is None:
        return ""
    return clean_text(text)


def type_of_schema(schema: dict | None) -> str:
    if not isinstance(schema, dict):
        return ""
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    if "type" in schema:
        t = schema["type"]
        if t == "array":
            items = schema.get("items", {})
            if isinstance(items, dict):
                if "$ref" in items:
                    return f"array<{items['$ref'].split('/')[-1]}>"
                if "type" in items:
                    return f"array<{items['type']}>"
            return "array"
        return str(t)
    if "allOf" in schema:
        return "allOf"
    if "oneOf" in schema:
        return "oneOf"
    if "anyOf" in schema:
        return "anyOf"
    return ""


def write_index(out_dir: Path, info: dict) -> None:
    lines = [
        "# v1 Baseline (Complete Reference)",
        "",
        "This section imports the Open Delivery v1 OpenAPI as a baseline reference in the current v2 documentation format.",
        "",
        "The goal is to keep full v1 coverage and evolve by delta as committee decisions for v2 are approved.",
        "",
        "## Source",
        "",
        "- OpenAPI: see local source file used for generation",
        f"- Version: `{md_escape(info.get('version', 'unknown'))}`",
        "",
        "## Contents",
        "",
        "- [General Rules and Security](security.md)",
        "- [REST Operations](operations.md)",
        "- [Webhooks](webhooks.md)",
        "- [Components: Schemas, Request Bodies, Responses](components.md)",
        "",
    ]
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_security(out_dir: Path, info: dict, components: dict) -> None:
    lines: list[str] = ["# General Rules and Security (v1)", "", "## API Metadata", ""]
    lines.append(f"- Title: `{md_escape(info.get('title'))}`")
    lines.append(f"- Version: `{md_escape(info.get('version'))}`")

    license_ = info.get("license", {})
    if isinstance(license_, dict):
        lines.append(
            f"- License: `{md_escape(license_.get('name'))}` ({md_escape(license_.get('url'))})"
        )

    contact = info.get("contact", {})
    if isinstance(contact, dict):
        lines.append(f"- Contact: `{md_escape(contact.get('url'))}`")

    lines.extend(["", "## Security Schemes", ""])
    for name, scheme in components.get("securitySchemes", {}).items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- Type: `{md_escape(scheme.get('type'))}`")
        if "in" in scheme:
            lines.append(f"- In: `{md_escape(scheme.get('in'))}`")
        if "name" in scheme:
            lines.append(f"- Header/Param Name: `{md_escape(scheme.get('name'))}`")
        if scheme.get("description"):
            lines.append(f"- Description: {md_escape(scheme.get('description'))}")
        flows = scheme.get("flows", {})
        if isinstance(flows, dict):
            for flow_name, flow in flows.items():
                lines.append(
                    f"- Flow `{flow_name}` token URL: `{md_escape(flow.get('tokenUrl'))}`"
                )
        lines.append("")

    lines.extend(["## Global Error Response Catalog", ""])
    responses = components.get("responses", {})
    if responses:
        lines.append("| Name | Description |")
        lines.append("|---|---|")
        for name, obj in responses.items():
            desc = obj.get("description") if isinstance(obj, dict) else ""
            lines.append(f"| `{md_escape(name)}` | {md_escape(desc)} |")

    (out_dir / "security.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_operations(out_dir: Path, paths: dict) -> None:
    lines: list[str] = ["# REST Operations (v1)", "", f"Total paths: **{len(paths)}**", ""]
    ordered_methods = ["get", "post", "put", "patch", "delete", "options", "head"]

    for path, methods in paths.items():
        lines.extend([f"## `{path}`", ""])
        if not isinstance(methods, dict):
            continue

        for method in ordered_methods:
            op = methods.get(method)
            if not isinstance(op, dict):
                continue

            lines.append(f"### `{method.upper()}`")
            lines.append(f"- OperationId: `{md_escape(op.get('operationId'))}`")
            lines.append(f"- Summary: {md_escape(op.get('summary'))}")

            tags = op.get("tags", [])
            if tags:
                lines.append("- Tags: " + ", ".join(f"`{md_escape(t)}`" for t in tags))

            security = op.get("security", "inherit")
            if security == []:
                lines.append("- Security: `none`")
            elif security == "inherit":
                lines.append("- Security: `inherit global/default`")
            elif isinstance(security, list):
                flattened: list[str] = []
                for item in security:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if isinstance(v, list) and v:
                                flattened.append(f"{k}({','.join(v)})")
                            else:
                                flattened.append(str(k))
                sec_str = ", ".join(f"`{md_escape(x)}`" for x in flattened) if flattened else "`configured`"
                lines.append("- Security: " + sec_str)
            else:
                lines.append("- Security: `configured`")

            params = op.get("parameters", [])
            if params:
                lines.extend([
                    "- Parameters:",
                    "",
                    "| Name | In | Required | Type |",
                    "|---|---|---|---|",
                ])
                for p in params:
                    if not isinstance(p, dict):
                        continue
                    ptype = type_of_schema(p.get("schema", {}) if isinstance(p.get("schema", {}), dict) else {})
                    lines.append(
                        f"| `{md_escape(p.get('name'))}` | `{md_escape(p.get('in'))}` | `{md_escape(p.get('required', False))}` | `{md_escape(ptype)}` |"
                    )
                lines.append("")

            req = op.get("requestBody")
            if req:
                if isinstance(req, dict) and "$ref" in req:
                    lines.append(f"- Request Body: `$ref` `{md_escape(req['$ref'])}`")
                elif isinstance(req, dict):
                    content = req.get("content", {})
                    if isinstance(content, dict) and content:
                        media = ", ".join(f"`{md_escape(k)}`" for k in content.keys())
                        lines.append(f"- Request Body Media Types: {media}")
                    else:
                        lines.append("- Request Body: present")

            responses = op.get("responses", {})
            if isinstance(responses, dict) and responses:
                lines.extend([
                    "- Responses:",
                    "",
                    "| HTTP | Description | Ref |",
                    "|---|---|---|",
                ])
                for code, robj in responses.items():
                    if isinstance(robj, dict):
                        desc = md_escape(robj.get("description"))
                        ref = md_escape(robj.get("$ref"))
                    else:
                        desc = ""
                        ref = ""
                    lines.append(f"| `{md_escape(code)}` | {desc} | `{ref}` |")
                lines.append("")

            lines.append("")

    (out_dir / "operations.md").write_text("\n".join(lines), encoding="utf-8")


def write_webhooks(out_dir: Path, webhooks: dict) -> None:
    lines: list[str] = ["# Webhooks (v1)", "", f"Total webhook paths: **{len(webhooks)}**", ""]
    ordered_methods = ["post", "put", "patch", "get", "delete"]

    for path, methods in webhooks.items():
        lines.extend([f"## `{path}`", ""])
        if not isinstance(methods, dict):
            continue

        for method in ordered_methods:
            op = methods.get(method)
            if not isinstance(op, dict):
                continue

            lines.append(f"### `{method.upper()}`")
            lines.append(f"- OperationId: `{md_escape(op.get('operationId'))}`")
            lines.append(f"- Summary: {md_escape(op.get('summary'))}")

            tags = op.get("tags", [])
            if tags:
                lines.append("- Tags: " + ", ".join(f"`{md_escape(t)}`" for t in tags))

            params = op.get("parameters", [])
            if params:
                lines.extend([
                    "",
                    "| Header/Param | In | Required |",
                    "|---|---|---|",
                ])
                for p in params:
                    if isinstance(p, dict):
                        lines.append(
                            f"| `{md_escape(p.get('name'))}` | `{md_escape(p.get('in'))}` | `{md_escape(p.get('required', False))}` |"
                        )
                lines.append("")

            responses = op.get("responses", {})
            if isinstance(responses, dict) and responses:
                lines.extend([
                    "",
                    "| HTTP | Description | Ref |",
                    "|---|---|---|",
                ])
                for code, robj in responses.items():
                    if isinstance(robj, dict):
                        desc = md_escape(robj.get("description"))
                        ref = md_escape(robj.get("$ref"))
                    else:
                        desc = ""
                        ref = ""
                    lines.append(f"| `{md_escape(code)}` | {desc} | `{ref}` |")
                lines.append("")

            lines.append("")

    (out_dir / "webhooks.md").write_text("\n".join(lines), encoding="utf-8")


def write_components(out_dir: Path, components: dict) -> None:
    lines: list[str] = ["# Components (v1)", "", "## Request Bodies", ""]

    request_bodies = components.get("requestBodies", {})
    if request_bodies:
        lines.extend([
            "| Name | Required | Media Types | Description |",
            "|---|---|---|---|",
        ])
        for name, body in request_bodies.items():
            required = body.get("required", False) if isinstance(body, dict) else False
            description = body.get("description", "") if isinstance(body, dict) else ""
            content = body.get("content", {}) if isinstance(body, dict) else {}
            media = ", ".join(f"`{md_escape(k)}`" for k in content.keys()) if isinstance(content, dict) else ""
            lines.append(
                f"| `{md_escape(name)}` | `{md_escape(required)}` | {media} | {md_escape(description)} |"
            )
    else:
        lines.append("_None_")

    lines.extend(["", "## Responses", ""])
    responses = components.get("responses", {})
    if responses:
        lines.extend(["| Name | Description |", "|---|---|"])
        for name, obj in responses.items():
            desc = obj.get("description") if isinstance(obj, dict) else ""
            lines.append(f"| `{md_escape(name)}` | {md_escape(desc)} |")
    else:
        lines.append("_None_")

    schemas = components.get("schemas", {})
    lines.extend(["", "## Schemas", "", f"Total schemas: **{len(schemas)}**", ""])

    for sname, sobj in schemas.items():
        lines.extend([f"### `{sname}`", ""])
        if not isinstance(sobj, dict):
            lines.extend(["- Type: `unknown`", ""])
            continue

        if sobj.get("type"):
            lines.append(f"- Type: `{md_escape(sobj.get('type'))}`")
        required = sobj.get("required", [])
        if isinstance(required, list) and required:
            lines.append("- Required fields: " + ", ".join(f"`{md_escape(x)}`" for x in required))
        discriminator = sobj.get("discriminator")
        if isinstance(discriminator, dict) and discriminator.get("propertyName"):
            lines.append(f"- Discriminator: `{md_escape(discriminator.get('propertyName'))}`")
        if sobj.get("description"):
            lines.append(f"- Description: {md_escape(sobj.get('description'))}")

        props = sobj.get("properties", {})
        if isinstance(props, dict) and props:
            lines.extend([
                "",
                "| Property | Type | Description |",
                "|---|---|---|",
            ])
            for pname, pobj in props.items():
                ptype = type_of_schema(pobj if isinstance(pobj, dict) else {})
                pdesc = md_escape(pobj.get("description")) if isinstance(pobj, dict) else ""
                lines.append(f"| `{md_escape(pname)}` | `{md_escape(ptype)}` | {pdesc} |")
            lines.append("")

        for comb in ("allOf", "oneOf", "anyOf"):
            if comb in sobj and isinstance(sobj[comb], list):
                refs: list[str] = []
                for entry in sobj[comb]:
                    if isinstance(entry, dict) and "$ref" in entry:
                        refs.append(f"`{md_escape(entry['$ref'])}`")
                    else:
                        refs.append("`inline schema`")
                lines.append(f"- {comb}: " + ", ".join(refs))

        lines.append("")

    (out_dir / "components.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate v1 baseline markdown docs from OpenAPI.")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to OpenAPI YAML file",
    )
    parser.add_argument(
        "--output",
        default="artifacts/v1-baseline",
        help="Output directory for generated files (default: artifacts/v1-baseline)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    info = data.get("info", {})
    paths = data.get("paths", {})
    webhooks = data.get("x-webhooks", {})
    components = data.get("components", {})

    write_index(output_dir, info)
    write_security(output_dir, info, components)
    write_operations(output_dir, paths)
    write_webhooks(output_dir, webhooks)
    write_components(output_dir, components)

    print(f"Generated v1 baseline docs in {output_dir}")


if __name__ == "__main__":
    main()
