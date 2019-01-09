#!/usr/bin/env python
# -*- coding: utf-8
import keyword
import os
import posixpath
import re
import shutil
from collections import namedtuple, defaultdict, Counter
from functools import total_ordering

import appdirs
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from jinja2 import Environment, FileSystemLoader

URL_TEMPLATE = "https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.{}/api/openapi-spec/swagger.json"
VERSION_RANGE = (6, 8)
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
    "string": "six.text_type",
    "date": "date",
    "DateTime": "datetime",
    "object": "dict",
    "file": "file",
    "binary": "bytes",
    "ByteArray": "bytes",
    "UUID": "str",
}
REF_PATTERN = re.compile(r"io\.k8s\.(.+)")
OPERATION_ID_TO_ACTION = {}
OPERATION_ID_TO_GVK = {}
PYTHON2_KEYWORDS = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec',
                    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass',
                    'print', 'raise', 'return', 'try', 'while', 'with', 'yield']

GVK = namedtuple("GVK", ("group", "version", "kind"))
Field = namedtuple("Field", ("name", "description", "type", "ref", "cls", "alt_type"))
Definition = namedtuple("Definition", ("name", "description", "fields", "gvks"))
Operation = namedtuple("Operation", ("path", "action"))


class Primitive(object):
    def __init__(self, type):
        self.name = TYPE_MAPPING.get(type, type)


@total_ordering
class Child(object):
    @property
    def parent_ref(self):
        return self.ref.rsplit(".", 1)[0]

    def __eq__(self, other):
        return self.ref == other.ref

    def __lt__(self, other):
        return self.ref < other.ref

    def __hash__(self):
        return hash(self.ref)


class Module(namedtuple("Module", ("ref", "name", "imports", "models")), Child):
    pass


class Model(Child):
    def __init__(self, ref, definition, operations=[]):
        self.ref = ref
        self.definition = definition
        self.operations = operations

    @property
    def name(self):
        return self.definition.name


class Package(namedtuple("Package", ("ref", "modules"))):
    @property
    def path(self):
        return self.ref.replace(".", os.sep)


class Import(namedtuple("Import", ("module", "models"))):
    @property
    def names(self):
        return sorted(m.definition.name for m in self.models)


def shorten_ref(id):
    m = REF_PATTERN.search(id)
    if not m:
        raise RuntimeError("Invalid id: {}".format(id))
    ref = m.group(1)
    return ref.replace(".pkg", "")


class PackageParser(object):
    _SPECIAL_TYPES = {
        shorten_ref("io.k8s.apimachinery.pkg.api.resource.Quantity"): Primitive("string"),
        shorten_ref("io.k8s.apimachinery.pkg.apis.meta.v1.Time"): Primitive("datetime.datetime"),
        shorten_ref("io.k8s.apimachinery.pkg.apis.meta.v1.MicroTime"): Primitive("datetime.datetime"),
        shorten_ref("io.k8s.apimachinery.pkg.apis.meta.v1.Patch"): Primitive("string"),
        shorten_ref("io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1beta1.CustomResourceSubresourceStatus"):
            Primitive("object"),  # This might not be the right thing to do, but the spec is unclear
        shorten_ref("io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1beta1.JSON"): Primitive("object"),
    }
    _UNION_TYPES = {
        shorten_ref("io.k8s.apimachinery.pkg.util.intstr.IntOrString"): (Primitive("string"), Primitive("integer")),
        shorten_ref("io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1beta1.JSONSchemaPropsOrArray"):
            (Primitive("dict"), Primitive("array")),
        shorten_ref("io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1beta1.JSONSchemaPropsOrBool"):
            (Primitive("dict"), Primitive("boolean")),
        shorten_ref("io.k8s.apiextensions-apiserver.pkg.apis.apiextensions.v1beta1.JSONSchemaPropsOrStringArray"):
            (Primitive("dict"), Primitive("array")),
    }

    def __init__(self, spec):
        self._spec = spec.get("definitions", {})
        self._packages = {}
        self._modules = {}
        self._models = {}
        self._gvk_lookup = {}

    def parse(self):
        self._parse_models()
        self._resolve_references()
        self._sort()
        return self._packages.values()

    def _parse_models(self):
        for id, item in self._spec.items():
            id = shorten_ref(id)
            package_ref, module_name, def_name = _split_ref(id)
            package = self.get_package(package_ref)
            module = self.get_module(package, module_name)
            gvks = []
            for x in item.get("x-kubernetes-group-version-kind", []):
                x = {k.lower(): v for k, v in x.items()}
                gvks.append(GVK(**x))
            fields = []
            required_fields = item.get("required", [])
            for field_name, property in item.get("properties", {}).items():
                fields.append(self._parse_field(field_name, property, required_fields))
            if not fields:
                print("Model {}.{}.{} has no fields, skipping".format(package_ref, module_name, def_name))
                continue
            definition = Definition(def_name, item.get("description", ""), fields, gvks)
            model = Model(_make_ref(package.ref, module.name, def_name), definition)
            module.models.append(model)
            self._models[model.ref] = model
            for gvk in gvks:
                self._gvk_lookup[gvk] = model
        print("Completed parse. Parsed {} packages, {} modules, {} models and {} GVKs.".format(len(self._packages),
                                                                                               len(self._modules),
                                                                                               len(self._models),
                                                                                               len(self._gvk_lookup)))

    def _parse_field(self, field_name, property, required_fields):
        field_type = property.get("type")
        field_ref = property.get("$ref")
        field_cls = "Field"
        description = property.get("description", "")
        if field_type == "array" and "items" in property:
            field_type = property["items"].get("type")
            field_ref = property["items"].get("$ref")
            field_cls = "ListField"
        elif ". Read-only." in description:
            field_cls = "ReadOnlyField"
        elif field_name in required_fields:
            field_cls = "RequiredField"
        if keyword.iskeyword(field_name):
            field_name = "_{}".format(field_name)
        field = Field(field_name, description, field_type, field_ref, field_cls, None)
        return field

    def get_package(self, package_ref):
        if package_ref not in self._packages:
            package = Package(package_ref, [])
            self._packages[package_ref] = package
        return self._packages[package_ref]

    def get_module(self, package, module_name):
        ref = _make_ref(package.ref, module_name)
        if ref not in self._modules:
            module = Module(ref, module_name, [], [])
            package.modules.append(module)
            self._modules[ref] = module
        return self._modules[ref]

    def get_model(self, package, module, def_name):
        ref = _make_ref(package.ref, module.name, def_name)
        return self._models[ref]

    def _resolve_references(self):
        for module in self._modules.values():
            imports = {}
            for model in module.models:
                self._resolve_fields(model.definition)
                for field in model.definition.fields:
                    ft = field.type
                    if isinstance(ft, Model):
                        if ft.parent_ref != model.parent_ref:
                            if ft.parent_ref not in imports:
                                package_ref, module_name, def_name = _split_ref(ft.ref)
                                package = self.get_package(package_ref)
                                ft_module = self.get_module(package, module_name)
                                imports[ft.parent_ref] = Import(ft_module, [])
                            imp = imports[ft.parent_ref]
                            if ft not in imp.models:
                                imp.models.append(ft)
            module.imports[:] = imports.values()

    def _resolve_fields(self, definition):
        new_fields = []
        for field in definition.fields:
            if field.ref and shorten_ref(field.ref) in self._UNION_TYPES:
                new_type, new_alt_type = self._UNION_TYPES[shorten_ref(field.ref)]
                new_field = field._replace(type=new_type, alt_type=new_alt_type)
            else:
                if field.ref:
                    field_type = self.resolve_ref(field.ref)
                else:
                    field_type = self._resolve_field(field.type)
                new_field = field._replace(type=field_type)
            if new_field.name in PYTHON2_KEYWORDS:
                new_field = new_field._replace(name="_{}".format(new_field.name))
            new_fields.append(new_field)
        definition.fields[:] = new_fields

    def resolve_ref(self, ref):
        if ref:
            ref_name = shorten_ref(ref)
            if ref_name in self._SPECIAL_TYPES:
                return self._SPECIAL_TYPES[ref_name]
            package_ref, module_name, def_name = _split_ref(ref_name)
            package = self.get_package(package_ref)
            module = self.get_module(package, module_name)
            model = self.get_model(package, module, def_name)
            return model

    def resolve_gvk(self, gvk):
        return self._gvk_lookup.get(gvk)

    def _resolve_field(self, type):
        if type:
            return Primitive(type)

    def _sort(self):
        for package in self._packages.values():
            for module in package.modules:
                module.imports.sort(key=lambda i: i.module.ref)
                module.models[:] = self._sort_models(module.models)

    def _sort_models(self, models):
        """We need to make sure that any model that references an other model comes later in the list"""
        Node = namedtuple("Node", ("model", "dependants", "dependencies"))
        nodes = {}
        for model in models:
            node = nodes.setdefault(model.ref, Node(model, [], []))
            for field in model.definition.fields:
                if isinstance(field.type, Model) and field.type.parent_ref == model.parent_ref:
                    dep = nodes.setdefault(field.type.ref, Node(field.type, [], []))
                    node.dependencies.append(dep)
        for node in sorted(nodes.values()):
            for dep in node.dependencies:
                dep.dependants.append(node)
        top_nodes = [n for n in nodes.values() if len(n.dependencies) == 0]
        top_nodes.sort()
        models = []
        while top_nodes:
            top_node = top_nodes.pop()
            models.append(top_node.model)
            for dep in top_node.dependants:
                dep.dependencies.remove(top_node)
                if len(dep.dependencies) == 0:
                    top_nodes.append(dep)
        return models


class ActionParser(object):
    def __init__(self, spec, package_parser):
        self._spec = spec.get("paths", {})
        self._package_parser = package_parser

    def parse(self):
        counter = Counter()
        operations = self._parse_operations()
        for gvk, actions in operations.items():
            model = self._package_parser.resolve_gvk(gvk)
            if not model:
                print("GVK {} resolved to no known model".format(gvk))
                continue
            model.operations = sorted(actions, key=lambda a: a.action)
            counter[model] += len(actions)
        print("Found {} actions distributed over {} models".format(sum(counter.values()), len(counter)))

    def _parse_operations(self):
        operations = defaultdict(list)
        for path, item in self._spec.items():
            if self._should_ignore_path(path):
                continue
            for method, operation in item.items():
                if self._should_ignore_method(method):
                    continue
                action = self._resolve_action(operation, path)
                if self._should_ignore_action(action):
                    continue
                gvk = self._resolve_gvk(operation)
                if gvk:
                    operations[gvk].append(Operation(path, action))
        return operations

    @staticmethod
    def _should_ignore_path(path):
        last = posixpath.split(path)[-1]
        return last in ("status", "scale", "rollback", "bindings", "log")

    @staticmethod
    def _should_ignore_method(method):
        return method in ("parameters", "patch")

    @staticmethod
    def _rename_action(action, path):
        if action.endswith("list"):
            if "{namespace}" not in path:
                action = "{}_all".format(action)
            else:
                action = "{}_ns".format(action)
        renames = {
            "post": "create",
            "put": "update"
        }
        return renames.get(action, action)

    @staticmethod
    def _should_ignore_action(action):
        return action in ("__undefined__", "patch", "deletecollection", "proxy", "connect")

    def _resolve_action(self, operation, path):
        op_id = operation.get("operationId")
        action = operation.get("x-kubernetes-action", "__undefined__")
        action = self._rename_action(action, path)
        if action == "__undefined__":
            return OPERATION_ID_TO_ACTION.get(op_id, action)
        OPERATION_ID_TO_ACTION[op_id] = action
        return action

    @staticmethod
    def _resolve_gvk(operation):
        op_id = operation.get("operationId")
        if "x-kubernetes-group-version-kind" not in operation:
            return OPERATION_ID_TO_GVK.get(op_id)
        gvk_data = operation["x-kubernetes-group-version-kind"]
        gvk = GVK(gvk_data["group"], gvk_data["version"], gvk_data["kind"])
        OPERATION_ID_TO_GVK[op_id] = gvk
        return gvk


class Generator(object):
    def __init__(self, packages, output_dir, version):
        self._packages = packages
        self._output_dir = output_dir
        self._version = version
        self._env = Environment(
            loader=FileSystemLoader(os.path.dirname(__file__)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self):
        print("Generating models in {}".format(self._output_dir))
        for package in self._packages:
            self._generate_package(package)
        for root, dirs, files in os.walk(self._output_dir):
            if "__init__.py" in files:
                continue
            with open(os.path.join(root, "__init__.py"), "w") as fobj:
                fobj.write("# Generated file")

    def _generate_package(self, package):
        package_dir = os.path.join(self._output_dir, package.path)
        if not os.path.isdir(package_dir):
            os.makedirs(package_dir)
        generated = False
        for module in package.modules:
            generated = self._generate_module(module, package_dir) or generated
        if not generated:
            print("Package {} had no modules, skipping".format(package.ref))
            shutil.rmtree(package_dir)
        else:
            print("Created package {}.".format(package.ref))

    def _generate_module(self, module, package_dir):
        if not module.models:
            print("Skipping module {}, as there are no models".format(module.ref))
            return False
        template = self._env.get_template("model.jinja2")
        module_path = os.path.join(package_dir, module.name) + ".py"
        with open(module_path, "w") as fobj:
            fobj.write(template.render(module=module, version=self._version))
        print("Generated module {}.".format(module.ref))
        return True


def _split_ref(s):
    s = s.replace("-", "_")
    return s.rsplit(".", 2)


def _make_ref(*args):
    return ".".join(args)


def _generate_version(version, url):
    print("=== Generating models for version {} ===".format(version))
    print("Getting spec at {}".format(url))
    resp = HTTP_CLIENT_SESSION.get(url)
    spec = resp.json()
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "k8s", "models", version)
    package_parser = PackageParser(spec)
    packages = package_parser.parse()
    action_parser = ActionParser(spec, package_parser)
    action_parser.parse()
    generator = Generator(packages, output_dir, version)
    generator.generate()


def main():
    for minor_version in reversed(range(*VERSION_RANGE)):
        version = "v1_{}".format(minor_version)
        url = URL_TEMPLATE.format(minor_version)
        _generate_version(version, url)


if __name__ == "__main__":
    main()
