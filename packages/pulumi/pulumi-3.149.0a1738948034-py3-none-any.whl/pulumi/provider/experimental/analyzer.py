# Copyright 2025, Pulumi Corporation.
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
import inspect
import sys
from collections.abc import Awaitable
from pathlib import Path
from types import GenericAlias, ModuleType
from typing import (
    Any,
    ForwardRef,
    Optional,
    Union,
    cast,
    get_args,
    get_origin,
)

from ...output import Output
from ...resource import ComponentResource
from .component import (
    ComponentDefinition,
    PropertyDefinition,
    PropertyType,
    TypeDefinition,
)
from .metadata import Metadata
from .util import camel_case

_NoneType = type(None)  # Available as typing.NoneType in >= 3.10


class TypeNotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(
            f"Could not find the type '{name}'. "
            + "Ensure it is defined in your source code or is imported."
        )


class DuplicateTypeError(Exception):
    def __init__(
        self, new_module: str, existing: Union[TypeDefinition, ComponentDefinition]
    ):
        self.new_module = new_module
        self.existing = existing
        super().__init__(
            f"Duplicate type '{existing.name}': orginally defined in '{existing.module}', but also found in '{new_module}'"
        )


class InvalidMapKeyError(Exception):
    def __init__(self, key_type: type, typ: type, property_name: str):
        self.key = key_type
        self.property = property_name
        self.typ = typ
        super().__init__(
            f"map keys must be strings, got '{key_type.__name__}' for '{typ.__name__}.{property_name}'"
        )


class Analyzer:
    """
    Analyzer searches a directory for subclasses of `ComponentResource` and
    infers a Pulumi Schema for these components based on type annotations.

    The entrypoint for this is `Analyzer.analyze`, which returns a dictionary of
    `ComponentDefinition`, which represent components, and a dictionary of
    `TypeDefinition`, which represent complex types, aka user defined types,
    used in the components inputs and/or outputs. This relies on a couple of
    assumptions:

    * Components are defined at the top level of the Python modules. Classes
      defined in a nested scope, such as a function, are not discovered.
      Essentially the analyser iterates over each element in `dir(module)` and
      looks for the subclasses at that level.
    * The names used in `ForwardRef`s can be resolved similarly.
    * The `__init__` method for each component has a typed argument named `args`
      which represent the inputs the component takes.
    * The types are put in a single Pulumi module, `index`. That is, all the Pulumi
      types have the typestring `<provider>:index:<type>`. This means that it is
      possible to have duplicate types, which raises an error durign analysis.

    To infer the schema, the analyzer follows the graph of types rooted at each
    component. From the component, it follows the `args` argument, and then
    follows each property of the args type. To implement recursive complex
    types, you have to use `ForwardRef`s
    https://docs.python.org/3/library/typing.html#typing.ForwardRef. The type a
    ForwardRef references is a string, which prevents us from following the
    "type pointer" to analyze it. If at the end of the analysis of a component
    we have unresolved forward references, the analyser resolves these by
    iterating over the Python modules in the same manner as it does to find the
    components.
    """

    def __init__(self, metadata: Metadata):
        self.metadata = metadata
        self.type_definitions: dict[str, TypeDefinition] = {}
        self.unresolved_forward_refs: dict[str, TypeDefinition] = {}

    def analyze(
        self, module_path: Path
    ) -> tuple[dict[str, ComponentDefinition], dict[str, TypeDefinition]]:
        """
        Analyze walks the directory at `path` and searches for
        ComponentResources in Python files.
        """
        components: dict[str, ComponentDefinition] = {}
        for file_path in self.iter(module_path):
            new_components = self.analyze_file(file_path, module_path)
            new_names = set(new_components.keys())
            old_names = set(components.keys())
            duplicates = old_names.intersection(new_names)
            if len(duplicates) > 0:
                name = duplicates.pop()
                duplicate = new_components[name]
                original = components[name]
                raise DuplicateTypeError(cast(str, duplicate.module), original)
            components.update(new_components)

        # Look for any forward references we could not resolve in the first
        # pass. This happens for types that are only ever referenced in
        # ForwardRefs.
        # With https://peps.python.org/pep-0649/ we might be able to let
        # Python handle this for us.
        for name, type_def in [*self.unresolved_forward_refs.items()]:
            a = self.find_type(module_path, type_def.name)
            (properties, properties_mapping) = self.analyze_type(a)
            type_def.properties = properties
            type_def.properties_mapping = properties_mapping
            del self.unresolved_forward_refs[name]

        return (components, self.type_definitions)

    def iter(self, path: Path):
        for file_path in sorted(path.glob("**/*.py")):
            if is_in_venv(file_path):
                continue
            yield file_path

    def analyze_file(
        self, file_path: Path, module_path: Path
    ) -> dict[str, ComponentDefinition]:
        components: dict[str, ComponentDefinition] = {}
        module_type = self.load_module(file_path, module_path)
        for name in dir(module_type):
            obj = getattr(module_type, name)
            if inspect.isclass(obj) and ComponentResource in obj.__bases__:
                components[name] = self.analyze_component(obj, module_path)
        return components

    def find_type(self, path: Path, name: str) -> type:
        """
        Find a type by name in the directory at `self.path`.

        :param name: The name of the type to find.
        """
        for file_path in self.iter(path):
            mod = self.load_module(file_path, path)
            comp = getattr(mod, name, None)
            if comp:
                return comp
        raise TypeNotFoundError(name)

    def load_module(self, file_path: Path, module_path: Path) -> ModuleType:
        name = file_path.name.replace(".py", "")
        rel_path = file_path.resolve().relative_to(module_path.resolve())
        spec = importlib.util.spec_from_file_location(str(rel_path), file_path)
        if not spec:
            raise Exception(f"Could not load module spec at {file_path}")
        module_type = importlib.util.module_from_spec(spec)
        sys.modules[name] = module_type
        if not spec.loader:
            raise Exception(f"Could not load module at {file_path}")
        spec.loader.exec_module(module_type)
        return module_type

    def get_annotations(self, o: Any) -> dict[str, Any]:
        if sys.version_info >= (3, 10):
            # Only available in 3.10 and later
            return inspect.get_annotations(o)
        else:
            # On Python 3.9 and older, __annotations__ is not guaranteed to be
            # present. Additionally, if the class has no annotations, and it is
            # a subclass, it will return the annotations of the parent
            # https://docs.python.org/3/howto/annotations.html#accessing-the-annotations-dict-of-an-object-in-python-3-9-and-older
            if isinstance(o, type):
                return o.__dict__.get("__annotations__", {})
            else:
                return getattr(o, "__annotations__", {})

    def analyze_component(
        self, component: type[ComponentResource], module_path: Path
    ) -> ComponentDefinition:
        ann = self.get_annotations(component.__init__)
        args = ann.get("args", None)
        if not args:
            raise Exception(
                f"ComponentResource '{component.__name__}' requires an argument named 'args' with a type annotation in its __init__ method"
            )

        (inputs, inputs_mapping) = self.analyze_type(args)
        (outputs, outputs_mapping) = self.analyze_type(component)
        return ComponentDefinition(
            name=component.__name__,
            description=component.__doc__.strip() if component.__doc__ else None,
            inputs=inputs,
            inputs_mapping=inputs_mapping,
            outputs=outputs,
            outputs_mapping=outputs_mapping,
            module=component.__module__,
        )

    def analyze_type(
        self, typ: type
    ) -> tuple[dict[str, PropertyDefinition], dict[str, str]]:
        """
        analyze_type returns a dictionary of the properties of a type based on
        its annotations, as well as a mapping from the schema property name
        (camel cased) to the Python property name.

        For example for the class

            class SelfSignedCertificateArgs:
                algorithm: pulumi.Output[str]
                rsa_bits: Optional[pulumi.Output[int]]

        we get the following properties and mapping:

            (
                {
                    "algorithm": SchemaProperty(type=PropertyType.STRING, optional=False),
                    "rsaBits": SchemaProperty(type=PropertyType.INTEGER, optional=True)
                },
                {
                    "algorithm": "algorithm",
                    "rsaBits": "rsa_bits"
                }
            )
        """
        ann = self.get_annotations(typ)
        mapping: dict[str, str] = {camel_case(k): k for k in ann.keys()}
        return {
            camel_case(k): self.analyze_property(v, typ, k) for k, v in ann.items()
        }, mapping

    def analyze_property(
        self,
        arg: type,
        typ: type,
        name: str,
        optional: Optional[bool] = None,
    ) -> PropertyDefinition:
        """
        analyze_property analyzes a single annotation and turns it into a SchemaProperty.

        :param arg: the type of the property we are analyzing
        :param typ: the type this property belongs to
        :param name: the name of the property
        :param optional: whether the property is optional or not
        """
        optional = optional if optional is not None else is_optional(arg)
        if is_plain(arg):
            # TODO: handle plain types
            return PropertyDefinition(
                type=py_type_to_property_type(arg),
                optional=optional,
            )
        elif is_input(arg):
            return self.analyze_property(
                unwrap_input(arg), typ, name, optional=optional
            )
        elif is_output(arg):
            return self.analyze_property(
                unwrap_output(arg), typ, name, optional=optional
            )
        elif is_optional(arg):
            return self.analyze_property(unwrap_optional(arg), typ, name, optional=True)
        elif is_list(arg):
            args = get_args(arg)
            items = self.analyze_property(args[0], typ, name)
            return PropertyDefinition(
                type=PropertyType.ARRAY, optional=optional, items=items
            )
        elif is_dict(arg):
            args = get_args(arg)
            if args[0] is not str:
                raise InvalidMapKeyError(args[0], typ, name)
            return PropertyDefinition(
                type=PropertyType.OBJECT,
                optional=optional,
                additional_properties=self.analyze_property(args[1], typ, name),
            )
        elif is_forward_ref(arg):
            name = cast(ForwardRef, arg).__forward_arg__
            type_def = self.type_definitions.get(name)
            # Forward references are assumed to be in the type's module.
            module = typ.__module__
            if type_def:
                if type_def.module != module:
                    raise DuplicateTypeError(module, type_def)
                # Forward ref to a type we saw before, return a reference to it.
                ref = f"#/types/{self.metadata.name}:index:{name}"
                return PropertyDefinition(
                    ref=ref,
                    optional=optional,
                )
            else:
                # Forward ref to a type we haven't seen yet. We create an empty
                # TypeDefiniton for it, and a return a PropertyDefinition that
                # references it. We also add it to the list of unresolved
                # forward references, so that we can come back to it after the
                # analysis is done.
                type_def = TypeDefinition(
                    name=name,
                    type="object",
                    properties={},
                    properties_mapping={},
                    module=module,
                )
                self.unresolved_forward_refs[name] = type_def
                self.type_definitions[type_def.name] = type_def
                ref = f"#/types/{self.metadata.name}:index:{type_def.name}"
                return PropertyDefinition(
                    ref=ref,
                    optional=optional,
                )
        elif not is_builtin(arg):
            # We have a custom type, analyze it recursively. Immediately add the
            # type definition to the list of type definitions, before calling
            # `analyze_type`, so we can resolve recursive forward references.
            name = arg.__name__
            type_def = self.type_definitions.get(name)
            if not type_def:
                type_def = TypeDefinition(
                    name=name,
                    type="object",
                    properties={},
                    properties_mapping={},
                    description=arg.__doc__,
                    module=arg.__module__,
                )
                self.type_definitions[type_def.name] = type_def
            else:
                if type_def.module and type_def.module != arg.__module__:
                    raise DuplicateTypeError(arg.__module__, type_def)
            (properties, properties_mapping) = self.analyze_type(arg)
            type_def.properties = properties
            type_def.properties_mapping = properties_mapping
            if type_def.name in self.unresolved_forward_refs:
                del self.unresolved_forward_refs[type_def.name]
            ref = f"#/types/{self.metadata.name}:index:{type_def.name}"
            return PropertyDefinition(
                ref=ref,
                optional=optional,
            )
        else:
            raise ValueError(f"unsupported type {arg}")


def is_in_venv(path: Path):
    venv = Path(sys.prefix).resolve()
    path = path.resolve()
    return venv in path.parents


def py_type_to_property_type(typ: type) -> PropertyType:
    if typ is str:
        return PropertyType.STRING
    if typ is int:
        return PropertyType.INTEGER
    if typ is float:
        return PropertyType.NUMBER
    if typ is bool:
        return PropertyType.BOOLEAN
    return PropertyType.OBJECT


def is_plain(typ: type) -> bool:
    return typ in (str, int, float, bool)


def is_optional(typ: type) -> bool:
    """
    A type is optional if it is a union that includes NoneType.
    """
    if get_origin(typ) == Union:
        return _NoneType in get_args(typ)
    return False


def unwrap_optional(typ: type) -> type:
    """
    Returns the first type of the Union that is not NoneType.
    """
    if not is_optional(typ):
        raise ValueError("Not an optional type")
    elements = get_args(typ)
    for element in elements:
        if element is not _NoneType:
            return element
    raise ValueError("Optional type with no non-None elements")


def is_output(typ: type):
    return get_origin(typ) == Output


def unwrap_output(typ: type) -> type:
    """Get the base type of an Output[T]"""
    if not is_output(typ):
        raise ValueError(f"{typ} is not an output type")
    args = get_args(typ)
    return args[0]


def is_input(typ: type) -> bool:
    """
    An input type is a Union that includes Awaitable, Output and a plain type.
    """
    origin = get_origin(typ)
    if origin is not Union:
        return False

    has_awaitable = False
    has_output = False
    has_plain = False
    for element in get_args(typ):
        if get_origin(element) is Awaitable:
            has_awaitable = True
        elif is_output(element):
            has_output = True
        elif is_forward_ref(element) and element.__forward_arg__ == "Output[T]":
            # In the core SDK, Input includes a forward reference to Output[T]
            has_output = True
        else:
            has_plain = True

    # We could try to be stricter here and ensure that the base type used in
    # Awaitable and Output is the same as the plain type. However, since Output
    # is a ForwardRef it is tricky to determine its base type. We could
    # potentially attempt to load the types using get_type_hints into an
    # environment that allows resolving the ForwardRef.
    if has_awaitable and has_output and has_plain:
        return True

    return False


def unwrap_input(typ: type) -> type:
    """Get the base type of an Input[T]"""
    if not is_input(typ):
        raise ValueError(f"{typ} is not an input type")
    # Look for the first Awaitable element and return its base type.
    for element in get_args(typ):
        if get_origin(element) is Awaitable:
            return get_args(element)[0]
    # Not reachable, we checked above that it is an input, which requires an
    # `Awaitable` element.
    raise ValueError("Input type with no Awaitable elements")


def is_forward_ref(typ: Any) -> bool:
    return isinstance(typ, ForwardRef)


def is_builtin(typ: type) -> bool:
    return typ.__module__ == "builtins"


def is_list(typ: type) -> bool:
    if isinstance(typ, GenericAlias):
        typ = get_origin(typ)
    return typ is list


def is_dict(typ: type) -> bool:
    if isinstance(typ, GenericAlias):
        typ = get_origin(typ)
    return typ is dict
