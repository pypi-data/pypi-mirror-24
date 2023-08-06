#     Copyright 2017, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Code generation contexts.

"""

import hashlib
import sys

from nuitka import Options
from nuitka.__past__ import iterItems
from nuitka.PythonVersions import python_version
from nuitka.utils.InstanceCounters import counted_del, counted_init

from .Namify import namifyConstant

# Many methods won't use self, but it's the interface. pylint: disable=no-self-use

class TempMixin(object):
    # Lots of details, everything gets to store bits here, to indicate
    # code generation states, and there are many, pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.tmp_names = {}
        self.tmp_types = {}
        self.forgotten_names = set()

        self.labels = {}

        # For exception handling
        self.needs_exception_variables = False
        self.exception_escape = None
        self.loop_continue = None
        self.loop_break = None

        # For branches
        self.true_target = None
        self.false_target = None

        self.keeper_variable_count = 0
        self.exception_keepers = (None, None, None, None)

        self.preserver_variable_counts = set()

        self.cleanup_names = []

        self.current_source_ref = None
        self.last_source_ref = None

    def getCurrentSourceCodeReference(self):
        return self.current_source_ref

    def setCurrentSourceCodeReference(self, value):
        result = self.current_source_ref
        self.current_source_ref = value

        if value is not None:
            self.last_source_ref = result

        return result

    def getLastSourceCodeReference(self):
        result = self.last_source_ref
        # self.last_source_ref = None
        return result

    def formatTempName(self, base_name, number):
        if number is None:
            return "tmp_{name}".format(
                name = base_name
            )
        else:
            return "tmp_{name}_{number:d}".format(
                name   = base_name,
                number = number
            )

    def allocateTempName(self, base_name, type_name = "PyObject *",
                         unique = False):
        if unique:
            number = None
        else:
            number = self.tmp_names.get(base_name, 0)
            number += 1

        self.tmp_names[base_name] = number

        if base_name not in self.tmp_types:
            self.tmp_types[base_name] = type_name
        else:
            assert self.tmp_types[base_name] == type_name, \
                (self.tmp_types[base_name], type_name)

        return self.formatTempName(
            base_name = base_name,
            number    = number
        )

    def getIntResName(self):
        return self.allocateTempName("res", "int", unique = True)

    def getBoolResName(self):
        return self.allocateTempName("result", "bool", unique = True)

    def hasTempName(self, base_name):
        return base_name in self.tmp_names

    def isUsed(self, tmp_name):
        if tmp_name.startswith("tmp_unused_"):
            return False
        else:
            return True

    def forgetTempName(self, tmp_name):
        self.forgotten_names.add(tmp_name)

    def getTempNameInfos(self):
        result  = []

        for base_name, count in sorted(iterItems(self.tmp_names)):
            if count is not None:
                for number in range(1,count+1):
                    tmp_name = self.formatTempName(
                        base_name = base_name,
                        number    = number
                    )

                    if tmp_name not in self.forgotten_names:
                        result.append(
                            (
                                tmp_name,
                                self.tmp_types[base_name]
                            )
                        )
            else:
                tmp_name = self.formatTempName(
                    base_name = base_name,
                    number    = None
                )

                if tmp_name not in self.forgotten_names:
                    result.append(
                        (
                            tmp_name,
                            self.tmp_types[base_name]
                        )
                    )

        return result

    def getExceptionEscape(self):
        return self.exception_escape

    def setExceptionEscape(self, label):
        result = self.exception_escape
        self.exception_escape = label
        return result

    def getLoopBreakTarget(self):
        return self.loop_break

    def setLoopBreakTarget(self, label):
        result = self.loop_break
        self.loop_break = label
        return result

    def getLoopContinueTarget(self):
        return self.loop_continue

    def setLoopContinueTarget(self, label):
        result = self.loop_continue
        self.loop_continue = label
        return result

    def allocateLabel(self, label):
        result = self.labels.get(label, 0)
        result += 1
        self.labels[label] = result

        return "{name}_{number:d}".format(
            name   = label,
            number = result
        )

    def needsExceptionVariables(self):
        return self.needs_exception_variables

    def markAsNeedsExceptionVariables(self):
        self.needs_exception_variables = True

    def allocateExceptionKeeperVariables(self):
        self.keeper_variable_count += 1

        return (
            "exception_keeper_type_%d" % self.keeper_variable_count,
            "exception_keeper_value_%d" % self.keeper_variable_count,
            "exception_keeper_tb_%d" % self.keeper_variable_count,
            "exception_keeper_lineno_%s" % self.keeper_variable_count
        )

    def getKeeperVariableCount(self):
        return self.keeper_variable_count

    def getExceptionKeeperVariables(self):
        return self.exception_keepers

    def setExceptionKeeperVariables(self, keeper_vars):
        result = self.exception_keepers
        self.exception_keepers = tuple(keeper_vars)
        return result

    def getExceptionPreserverCounts(self):
        return self.preserver_variable_counts

    def addExceptionPreserverVariables(self, count):
        assert count != 0
        self.preserver_variable_counts.add(count)

    def getTrueBranchTarget(self):
        return self.true_target

    def getFalseBranchTarget(self):
        return self.false_target

    def setTrueBranchTarget(self, label):
        self.true_target = label

    def setFalseBranchTarget(self, label):
        self.false_target = label

    def getCleanupTempnames(self):
        return self.cleanup_names[-1]

    def addCleanupTempName(self, tmp_name):
        assert tmp_name not in self.cleanup_names[-1], tmp_name

        self.cleanup_names[-1].append(tmp_name)

    def removeCleanupTempName(self, tmp_name):
        assert tmp_name in self.cleanup_names[-1], tmp_name
        self.cleanup_names[-1].remove(tmp_name)

    def needsCleanup(self, tmp_name):
        return tmp_name in self.cleanup_names[-1]

    def pushCleanupScope(self):
        self.cleanup_names.append([])

    def popCleanupScope(self):
        assert not self.cleanup_names[-1]
        del self.cleanup_names[-1]


class CodeObjectsMixin(object):
    def __init__(self):
        # Code objects needed made unique by a key.
        self.code_objects = {}

    def getCodeObjects(self):
        return sorted(iterItems(self.code_objects))

    def getCodeObjectHandle(self, code_object):
        key = (
            code_object.getFilename(),
            code_object.getCodeObjectName(),
            code_object.getLineNumber(),
            code_object.getVarNames(),
            code_object.getArgumentCount(),
            code_object.getKwOnlyParameterCount(),
            code_object.getCodeObjectKind(),
            code_object.getFlagIsOptimizedValue(),
            code_object.getFlagNewLocalsValue(),
            code_object.hasStarListArg(),
            code_object.hasStarDictArg(),
            code_object.getFlagHasClosureValue(),
            code_object.getFutureSpec().asFlags()
        )

        if key not in self.code_objects:
            self.code_objects[key] = "codeobj_%s" % self._calcHash(key)

        return self.code_objects[key]

    if python_version < 300:
        def _calcHash(self, key):
            hash_value = hashlib.md5(
                "%s%s%d%s%d%d%s%s%s%s%s%s%s" % key
            )

            return hash_value.hexdigest()
    else:
        def _calcHash(self, key):
            hash_value = hashlib.md5(
                ("%s%s%d%s%d%d%s%s%s%s%s%s%s" % key).encode("utf-8")
            )

            return hash_value.hexdigest()


class PythonContextBase(object):
    @counted_init
    def __init__(self):
        self.source_ref = None

    __del__ = counted_del()


class PythonChildContextBase(PythonContextBase):
    def __init__(self, parent):
        PythonContextBase.__init__(self)

        self.parent = parent

    def getConstantCode(self, constant):
        return self.parent.getConstantCode(constant)

    def getModuleCodeName(self):
        return self.parent.getModuleCodeName()

    def getModuleName(self):
        return self.parent.getModuleName()

    def addHelperCode(self, key, code):
        return self.parent.addHelperCode(key, code)

    def hasHelperCode(self, key):
        return self.parent.hasHelperCode(key)

    def addDeclaration(self, key, code):
        self.parent.addDeclaration(key, code)

    def pushFrameVariables(self, frame_variables):
        return self.parent.pushFrameVariables(frame_variables)

    def popFrameVariables(self):
        return self.parent.popFrameVariables()

    def getFrameVariableTypeDescriptions(self):
        return self.parent.getFrameVariableTypeDescriptions()

    def getFrameVariableTypeDescription(self):
        return self.parent.getFrameVariableTypeDescription()

    def getFrameVariableCodeNames(self):
        return self.parent.getFrameVariableCodeNames()

def _getConstantDefaultPopulation():
    # Note: Can't work with set here, because we need to put in some values that
    # cannot be hashed.

    result = [
        # Basic values that the helper code uses all the times.
        (),
        {},
        "",
        True,
        False,
        0,
        1,

        # For Python3 empty bytes, no effect for Python2, same as "", used for
        # code objects.
        b"",

        # Python mechanics, used in various helpers.
        "__module__",
        "__class__",
        "__name__",
        "__metaclass__",
        "__dict__",
        "__doc__",
        "__file__",
        "__path__",
        "__enter__",
        "__exit__",
        "__builtins__",
        "__all__",
        "__cmp__",
        "__iter__",

        # Patched module name.
        "inspect",

        # Names of built-ins used in helper code.
        "compile",
        "range",
        "open",
        "sum",
        "format",
        "__import__",
        "bytearray",
        "staticmethod",
        "classmethod",

        # Arguments of __import__ built-in used in helper code.
        "name",
        "globals",
        "locals",
        "fromlist",
        "level"
    ]

    if python_version >= 300:
        # For Python3 modules
        result += (
            "__cached__",
            "__loader__",
        )

        # For Python3 print
        result += (
            "print",
            "end",
            "file"
        )

        # For Python3 bytes built-in.
        result += (
            "bytes",
        )

    if python_version >= 330:
        # Modules have that attribute starting with 3.3
        result.append(
            "__loader__"
        )

    if python_version >= 340:
        result.append(
            # YIELD_FROM uses this starting 3.4, with 3.3 other code is used.
            "send"
        )

    if python_version >= 330:
        result += (
            # YIELD_FROM uses this
            "throw",
            "close",
        )


    if python_version < 300:
        # For patching Python2 internal class type
        result += (
            "__getattr__",
            "__setattr__",
            "__delattr__",
        )

        # For patching Python2 "sys" attributes for current exception
        result += (
            "exc_type",
            "exc_value",
            "exc_traceback"
        )

    # The xrange built-in is Python2 only.
    if python_version < 300:
        result.append(
            "xrange"
        )

    # Executables only
    if not Options.shallMakeModule():
        result.append(
            "__main__"
        )

        # The "site" module is referenced in inspect patching.
        result.append(
            "site"
        )

    # Built-in original values
    if not Options.shallMakeModule():
        result += [
            "type",
            "len",
            "range",
            "repr",
            "int",
            "iter",
        ]

        if python_version < 300:
            result.append(
                "long",
            )

    # Disabling warnings at startup
    if "no_warnings" in Options.getPythonFlags():
        result.append(
            "ignore"
        )

    if python_version >= 350:
        # Patching the types module.
        result.append(
            "types"
        )

    if not Options.shallMakeModule():
        result.append(
            sys.executable
        )

    return result


class PythonGlobalContext(object):
    def __init__(self):
        self.constants = {}
        self.constant_use_count = {}

        for constant in _getConstantDefaultPopulation():
            code = self.getConstantCode(constant)

            # Force them to be global.
            self.countConstantUse(code)
            self.countConstantUse(code)

        self.needs_exception_variables = False

    def getConstantCode(self, constant):
        # Use in user code, or for constants building code itself, many
        # constant types get special code immediately.
        # pylint: disable=too-many-branches
        if constant is None:
            key = "Py_None"
        elif constant is True:
            key = "Py_True"
        elif constant is False:
            key = "Py_False"
        elif constant is Ellipsis:
            key = "Py_Ellipsis"
        elif type(constant) is type:
            # TODO: Maybe make this a mapping in nuitka.Builtins

            if constant is None:
                key = "(PyObject *)Py_TYPE( Py_None )"
            elif constant is object:
                key = "(PyObject *)&PyBaseObject_Type"
            elif constant is staticmethod:
                key = "(PyObject *)&PyStaticMethod_Type"
            elif constant is classmethod:
                key = "(PyObject *)&PyClassMethod_Type"
            elif constant is bytearray:
                key = "(PyObject *)&PyByteArray_Type"
            elif constant is enumerate:
                key = "(PyObject *)&PyEnum_Type"
            elif constant is frozenset:
                key = "(PyObject *)&PyFrozenSet_Type"
            elif python_version >= 270 and constant is memoryview:
                key = "(PyObject *)&PyMemoryView_Type"
            elif python_version < 300 and constant is basestring: # pylint: disable=I0021,undefined-variable
                key = "(PyObject *)&PyBaseString_Type"
            elif python_version < 300 and constant is xrange: # pylint: disable=I0021,undefined-variable
                key = "(PyObject *)&PyRange_Type"
            else:
                type_name = constant.__name__

                if constant is int and python_version >= 300:
                    type_name = "long"
                elif constant is str:
                    type_name = "string" if python_version < 300 else "unicode"

                key = "(PyObject *)&Py%s_Type" % type_name.title()
        else:
            key = "const_" + namifyConstant(constant)

        if key not in self.constants:
            self.constants[key] = constant

        return key

    def countConstantUse(self, constant):
        if constant not in self.constant_use_count:
            self.constant_use_count[constant] = 0

        self.constant_use_count[constant] += 1

    def getConstantUseCount(self, constant):
        return self.constant_use_count[constant]

    def getConstants(self):
        return self.constants


class FrameDeclarationsMixin(object):
    def __init__(self):
        self.frame_declarations = []

        # Frame is active or not, default not.
        self.frame_variables_stack = [""]
        # Type descriptions of the current frame.
        self.frame_type_descriptions = [()]

        # Indicator if the "type_description" is needed.
        self.needs_type_description = False

        # Types of variables for current frame.
        self.variable_types = {}

        # Currently active frame code identifier.
        self.frame_handle = None


    def getFrameHandle(self):
        return self.frame_handle

    def setFrameHandle(self, frame_handle):
        self.frame_handle = frame_handle

    def addFrameDeclaration(self, frame_decl):
        self.frame_declarations.append(frame_decl)

    def getFrameDeclarations(self):
        return self.frame_declarations

    def pushFrameVariables(self, frame_variables):
        """ Set current the frame variables. """
        self.frame_variables_stack.append(frame_variables)
        self.frame_type_descriptions.append(set())

    def popFrameVariables(self):
        """ End of frame, remove it. """
        del self.frame_variables_stack[-1]
        del self.frame_type_descriptions[-1]

    def setVariableType(self, variable, variable_code_name, variable_c_type):
        assert variable.isLocalVariable(), variable

        self.variable_types[variable.getName()] = variable_code_name, variable_c_type.getTypeIndicator()

    def getFrameVariableTypeDescriptions(self):
        return self.frame_type_descriptions[-1]

    def getFrameVariableTypeDescription(self):
        result = "".join(
            self.variable_types.get(var_name, ("NULL", 'N'))[1]
            for var_name in
            self.frame_variables_stack[-1]
        )

        if result:
            self.frame_type_descriptions[-1].add(result)

        return result

    def getFrameVariableCodeNames(self):
        def casted(var_name):
            variable_desc = self.variable_types.get(var_name, ("NULL", 'N'))

            if variable_desc[1] in ('b',):
                return "(int)" + variable_desc[0]
            else:
                return variable_desc[0]

        return ", ".join(
            casted(var_name)
            for var_name in
            self.frame_variables_stack[-1]
        )

    def needsFrameVariableTypeDescription(self):
        return self.needs_type_description

    def markAsNeedsFrameVariableDescription(self):
        self.needs_type_description = True


class PythonModuleContext(PythonContextBase, TempMixin, CodeObjectsMixin,
                          FrameDeclarationsMixin):
    # Plenty of attributes, because it's storing so many different things.
    # pylint: disable=too-many-instance-attributes

    def __init__(self, module, module_name, code_name, filename, global_context):
        PythonContextBase.__init__(self)

        TempMixin.__init__(self)
        CodeObjectsMixin.__init__(self)
        FrameDeclarationsMixin.__init__(self)

        self.module = module
        self.name = module_name
        self.code_name = code_name
        self.filename = filename

        self.global_context = global_context

        self.declaration_codes = {}
        self.helper_codes = {}

        self.constants = set()

        self.return_release_mode = False

        self.frame_handle = None

        self.return_exit = True

        self.return_name = None

        self.needs_module_filename_object = False

    def __repr__(self):
        return "<PythonModuleContext instance for module %s>" % self.filename

    def getOwner(self):
        return self.module

    def isCompiledPythonModule(self):
        return True

    def hasLocalsDict(self):
        return False

    def getName(self):
        return self.name

    def getFilename(self):
        return self.filename

    def mayRaiseException(self):
        body = self.module.getBody()

        return body is not None and body.mayRaiseException(BaseException)

    getModuleName = getName

    def getModuleCodeName(self):
        return self.code_name

    def setFrameGuardMode(self, guard_mode):
        assert guard_mode == "once"

    def addHelperCode(self, key, code):
        assert key not in self.helper_codes, key

        self.helper_codes[ key ] = code

    def hasHelperCode(self, key):
        return key in self.helper_codes

    def getHelperCodes(self):
        return self.helper_codes

    def addDeclaration(self, key, code):
        assert key not in self.declaration_codes

        self.declaration_codes[ key ] = code

    def getDeclarations(self):
        return self.declaration_codes

    def getReturnValueName(self):
        return self.return_name

    def setReturnValueName(self, value):
        result = self.return_name
        self.return_name = value
        return result

    def setReturnReleaseMode(self, value):
        result = self.return_release_mode
        self.return_release_mode = value
        return result

    def getReturnReleaseMode(self):
        return self.return_release_mode

    def getReturnTarget(self):
        return self.return_exit

    def setReturnTarget(self, label):
        result = self.return_exit
        self.return_exit = label
        return result

    def mayRecurse(self):
        return False

    def getConstantCode(self, constant):
        result = self.global_context.getConstantCode(constant)

        if result not in self.constants:
            self.constants.add(result)
            self.global_context.countConstantUse(result)

        return result

    def getConstants(self):
        return self.constants

    def markAsNeedsModuleFilenameObject(self):
        self.needs_module_filename_object = True

    def needsModuleFilenameObject(self):
        return self.needs_module_filename_object


class PythonFunctionContext(FrameDeclarationsMixin, PythonChildContextBase, TempMixin):
    def __init__(self, parent, function):
        PythonChildContextBase.__init__(
            self,
            parent = parent
        )

        TempMixin.__init__(self)
        FrameDeclarationsMixin.__init__(self)

        self.function = function

        self.return_exit = None

        self.setExceptionEscape("function_exception_exit")
        self.setReturnTarget("function_return_exit")

        self.return_release_mode = False
        self.return_name = None

        self.frame_handle = None

    def __repr__(self):
        return "<PythonFunctionContext for %s '%s'>" % (
            "function" if not self.function.isExpressionClassBody() else "class",
            self.function.getName()
        )

    def getFunction(self):
        return self.function

    def getOwner(self):
        return self.function

    def hasLocalsDict(self):
        return self.function.hasLocalsDict()

    def getReturnValueName(self):
        if self.return_name is None:
            self.return_name = self.allocateTempName("return_value", unique = True)

        return self.return_name

    def setReturnValueName(self, value):
        result = self.return_name
        self.return_name = value
        return result

    def getReturnTarget(self):
        return self.return_exit

    def setReturnTarget(self, label):
        result = self.return_exit
        self.return_exit = label
        return result

    def setReturnReleaseMode(self, value):
        result = self.return_release_mode
        self.return_release_mode = value
        return result

    def getReturnReleaseMode(self):
        return self.return_release_mode

    def mayRecurse(self):
        # TODO: Determine this at compile time for enhanced optimizations.
        return True

    def getCodeObjectHandle(self, code_object):
        return self.parent.getCodeObjectHandle(code_object)


class PythonFunctionDirectContext(PythonFunctionContext):
    def isForDirectCall(self):
        return True

    def isForCrossModuleUsage(self):
        return self.function.isCrossModuleUsed()

    def isForCreatedFunction(self):
        return False


class PythonGeneratorObjectContext(PythonFunctionContext):
    def isForDirectCall(self):
        return False

    def isForCrossModuleUsage(self):
        return self.function.isCrossModuleUsed()

    def isForCreatedFunction(self):
        return False

    def getContextObjectName(self):
        return "generator"

    def getGeneratorReturnValueName(self):
        if python_version >= 330:
            return self.allocateTempName(
                "return_value",
                "PyObject *",
                unique = True
            )
        else:
            return self.allocateTempName(
                "generator_return",
                "bool",
                unique = True
            )


class PythonCoroutineObjectContext(PythonGeneratorObjectContext):
    def getContextObjectName(self):
        return "coroutine"


class PythonAsyncgenObjectContext(PythonGeneratorObjectContext):
    def getContextObjectName(self):
        return "asyncgen"


class PythonFunctionCreatedContext(PythonFunctionContext):
    def isForDirectCall(self):
        return False

    def isForCreatedFunction(self):
        return True
