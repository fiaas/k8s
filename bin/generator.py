#!/usr/bin/env python
# -*- coding: utf-8

import os
from collections import namedtuple, defaultdict
from pprint import pprint

import appdirs
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from jinja2 import Environment, FileSystemLoader

SPEC_URL = "https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.12/api/openapi-spec/swagger.json"
HTTP_CLIENT_SESSION = CacheControl(requests.session(), cache=FileCache(appdirs.user_cache_dir("k8s-generator")))

GVK = namedtuple("GVK", ("group", "version", "kind"))
Field = namedtuple("Field", ("name", "description", "type", "ref"))
Definition = namedtuple("Definition", ("package", "name", "description", "fields"))
Operation = namedtuple("Operation", ("path", "action", "description"))
Model = namedtuple("Model", ("gvk", "definition", "operations"))
Import = namedtuple("Import", ("package", "name"))


def _parse_definitions(definitions):
    result = defaultdict(list)
    for id, item in definitions.items():
        package, kind = id[len("io.k8s."):].rsplit(".", 1)
        package = package.replace("-", "_")
        gvks = item.get("x-kubernetes-group-version-kind")
        if not gvks:
            continue
        keys = (GVK(**x) for x in gvks)
        fields = []
        for name, property in item["properties"].items():
            fields.append(Field(name, property.get("description", ""), property.get("type"), property.get("$ref")))
        definition = Definition(package, kind, item.get("description", ""), fields)
        for key in keys:
            result[key].append(definition)
    total = sum(len(x) for x in result.values())
    print("Extracted {} gvks, with {} definitions in total".format(len(result), total))
    return result


def _parse_paths(paths):
    result = defaultdict(list)
    for id, item in paths.items():
        methods = (p for p in item.keys() if p not in ("parameters", "$ref"))
        for method in methods:
            operation = item[method]
            gvks = operation.get("x-kubernetes-group-version-kind")
            if not gvks:
                continue
            key = GVK(**gvks)
            action = operation.get("x-kubernetes-action")
            if not action:
                continue
            o = Operation(id, action, operation.get("description", ""))
            result[key].append(o)
    total = sum(len(x) for x in result.values())
    print("Extracted {} gvks, with {} operations in total".format(len(result), total))
    return result


def _make_models(definitions, operations):
    result = defaultdict(list)
    for gvk in definitions.keys():
        print("Generating model for {}, based on this definition:".format(gvk))
        pprint(definitions[gvk])
        definition = definitions[gvk][-1]
        result[definition.package].append(Model(gvk, definition, operations[gvk]))
    print("Collected {} models in total".format(len(result)))
    return result


def _generate_package(package, models, imports, output_dir):
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    file_path = os.path.join(output_dir, package.replace(".", os.sep))
    package_dir = os.path.dirname(file_path)
    if not os.path.isdir(package_dir):
        os.makedirs(package_dir)
    for root, dirs, files in os.walk(output_dir):
        if "__init__.py" in files:
            continue
        with open(os.path.join(root, "__init__.py"), "w") as fobj:
            fobj.write("# Generated file")
    template = env.get_template("model.jinja2")
    with open(file_path, "w") as fobj:
        fobj.write(template.render(models=models, imports=imports))


def _resolve_ref(ref):
    return ref[len("#/definitions/io.k8s."):]


def _resolve_types(package, models):
    imports = set()
    for model in models:
        new_fields = []
        for field in model.definition.fields:
            if field.ref:
                field_type = _resolve_ref(field.ref)
            else:
                field_type = field.type
            if "." in field_type:
                if not field_type.startswith(package):
                    field_package, field_type = field_type.rsplit(".", 1)
                    imports.add(Import(field_package, field_type))
            new_fields.append(field._replace(type=field_type))
        model.definition.fields[:] = new_fields
    return imports


def main():
    resp = HTTP_CLIENT_SESSION.get(SPEC_URL)
    spec = resp.json()
    for key in ("paths", "definitions", "parameters", "responses", "securityDefinitions", "security", "tags"):
        print("Specification contains {} {}".format(len(spec.get(key, [])), key))
    pprint(spec["info"])
    definitions = _parse_definitions(spec["definitions"])
    operations = _parse_paths(spec["paths"])
    models = _make_models(definitions, operations)
    for package, models in models.items():
        imports = _resolve_types(package, models)
        _generate_package(package, models, imports,
                          os.path.join(os.path.dirname(os.path.dirname(__file__)), "k8s", "models"))


if __name__ == "__main__":
    main()
