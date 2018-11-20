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
TYPE_MAPPING = {
    "integer": "int",
    "float": "float",
    "number": "float",
    "long": "int",
    "double": "float",
    "array": "list",
    "map": "dict",
    "boolean": "bool",
    "string": "str",
    "date": "date",
    "DateTime": "datetime",
    "object": "dict",
    "file": "file",
    "binary": "bytes",
    "ByteArray": "bytes",
    "UUID": "str",
}

GVK = namedtuple("GVK", ("group", "version", "kind"))
Field = namedtuple("Field", ("name", "description", "type", "ref"))
Definition = namedtuple("Definition", ("package", "name", "description", "fields", "gvks"))
Operation = namedtuple("Operation", ("path", "action", "description"))
Model = namedtuple("Model", ("definition", "operations"))
Import = namedtuple("Import", ("package", "name"))


def _parse_definitions(definitions):
    result = {}
    for id, item in definitions.items():
        package, name = id[len("io.k8s."):].rsplit(".", 1)
        package = package.replace("-", "_")
        gvks = [GVK(**x) for x in item.get("x-kubernetes-group-version-kind", [])]
        fields = []
        for field_name, property in item.get("properties", {}).items():
            fields.append(Field(field_name, property.get("description", ""), property.get("type"), property.get("$ref")))
        definition = Definition(package, name, item.get("description", ""), fields, gvks)
        key = (package, name)
        result[key] = definition
    print("Extracted {} definitions in total".format(len(result)))
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
    for key in definitions.keys():
        package, name = key
        print("Generating model for {}.{}, based on this definition:".format(package, name))
        definition = definitions[key]
        pprint(definition)
        result[definition.package].append(Model(definition, None))
    print("Collected {} models in total".format(len(result)))
    return result


def _generate_package(package, models, imports, output_dir):
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(__file__)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    file_path = os.path.join(output_dir, package.replace(".", os.sep)) + ".py"
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
                field_type = TYPE_MAPPING.get(field.type, field.type)
            if "." in field_type:
                if not field_type.startswith(package):
                    field_package, field_type = field_type.rsplit(".", 1)
                    imports.add(Import(field_package, field_type))
                else:
                    field_type = field_type[len(package)+1:]
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
    #operations = _parse_paths(spec["paths"])
    models = _make_models(definitions, None)
    for package, models in models.items():
        imports = _resolve_types(package, models)
        _generate_package(package, models, imports,
                          os.path.join(os.path.dirname(os.path.dirname(__file__)), "k8s", "models"))


if __name__ == "__main__":
    main()
