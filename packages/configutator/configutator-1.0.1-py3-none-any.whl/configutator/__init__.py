import re, os, pickle
from getopt import gnu_getopt
from inspect import signature, getdoc, getfile, Parameter

from .tator import normaliseArgs
from .valitator import validate

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap
import jmespath

from asciimatics.screen import Screen, StopApplication
from asciimatics.scene import Scene
import asciimatics.widgets as Widgets
from asciimatics.event import KeyboardEvent

YAMLLoader = ruamel.yaml.SafeLoader

funcDocRegex = re.compile(r'^[^:]+?(?=[\s]*:[\w]+)')
argDocRegEx = re.compile(r':param ([^:]+):[\t ]*(.+)$', flags=re.MULTILINE)

def getParamDoc(func) -> dict:
    """
    Helper to parse out parameter documentation using :data:`argDocRegEx`
    :param func: The function to retrieve the docstring using :func:`inspect.getdoc`
    :return: dictionary of documentation keyed on parameter name
    """
    return {match.group(1): match.group(2) for match in argDocRegEx.finditer(getdoc(func) or "")}

def getTrueAnnotationType(annotation):
    """
    Resolve the supertype of an annotation type possibly created using the typing module.
    :param annotation: A type object.
    :return: The original object or its supertype.
    """
    return getattr(annotation, '__supertype__', annotation)

def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.

    Taken from distutils.util and modified to return correct type.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

def generate(functions: list) -> dict:
    """
    Attempt to create a configuration yaml node for a list of functions.
    :param functions: List of functions to create a config for.
    :return: dictionary of required config parameters
    """
    config = {}
    for func in functions:
        sig = signature(func)
        params = CommentedMap()
        params.update({name:None if param.default == Parameter.empty else param.default for name, param in sig.parameters})
        for match in argDocRegEx.finditer(getdoc(func)):
            params.yaml_add_eol_comment(match.group(2), match.group(1))
        config[func.__name__] = params
    return config

class TransformArg:
    """
    Used to transform argument values to the intended type
    """
    __slots__ = 'xform'
    def __init__(self, xform=None):
        """
        Constructor.
        :param xform: A single parameter function that accepts the passed argument string or a three element tuple.
                      The tuple must be of the form (function, tuple with arguments or None, tuple with arguments or None).
                      The value is passed to the function wrapped between the values specified in the second and third tuples.
                      ie. xform=(open, None, 'w+')
        """
        if isinstance(xform, tuple) and len(xform) < 3:
            raise ValueError("xform tuple must be of size 3")
        self.xform = xform
        super().__init__()

    def __call__(self, value):
        if self.xform:
            args = (value,)
            if isinstance(self.xform, tuple):
                if self.xform[1]:
                    args = self.xform[1] + args
                if self.xform[2]:
                    args = args + self.xform[2]
                return self.xform[0](*args)
            return self.xform(*args)
        else:
            return value

# -- Config file mapping --

class TransformCfg(TransformArg):
    """
    Extends :class:`TransformArg` to handle JMESPath expressions for config mapping
    """
    __slots__ = 'expression'
    def __init__(self, path: str, xform=None):
        """

        :param path: A valid JMESPath that returns the intended config value
        :param xform: See :meth:`TransformArg.__init__`
        """
        super().__init__(xform)
        self.expression = jmespath.compile(path) if path else None

def ConfigMap(*args, **kwargs):
    """
    Function decorator that specifies parameter mappings to a yaml structure.
    The values of the arguments should either be a string with a JMESPath expression mapping to the intended config node,
    None to have configutator ignore the parameter when mapping, or a :class:`TransformCfg` instance.
    Gives the decorated function object a __cfgMap__ attribute.
    :param args: Positional arguments that coincide with the arguments of the function to decorate.
    :param kwargs: Keyword arguments that coincide with the arguments of the function to decorate. This will override anything conflicting with args.
    :return: A function that will add the specified mappings to the function passed to its single argument.
    """
    def wrap(func):
        sig = signature(func)
        nArgs = normaliseArgs(func, args, kwargs)
        if not hasattr(func, '__cfgMap__'):
            func.__cfgMap__ = {}
        if '_func' in nArgs:
            func.__cfgMap__['_func'] = jmespath.compile(nArgs['_func'])
        for name in sig.parameters:
            if name in nArgs:
                expression = nArgs.get(name)
                if isinstance(expression, TransformCfg):
                    func.__cfgMap__[name] = expression
                else:
                    func.__cfgMap__[name] = jmespath.compile(expression) if expression else None
            elif name not in func.__cfgMap__:
                func.__cfgMap__[name] = jmespath.compile(name)

        return func
    return wrap

def mapConfig(func, yaml_node, path = None) -> dict:
    """
    Maps yaml configuration nodes to the specified functions parameters.
    :param func: The function to map its parameters. Should have been decorated by @ConfigMap, if not will default to function variable names as the JMESPath expression.
    :param yaml_node: The root yaml node to search.
    :param path: If specified, will override the functions '_func' property specified by @ConfigMap.
    :return: A dict keyed on the func's parameter names with the values found in the passed yaml node.
    """
    if path:
        yaml_node = yaml_node.get(path, yaml_node)
    elif hasattr(func, '__cfgMap__') and '_func' in func.__cfgMap__:
        yaml_node = func.__cfgMap__['_func'].search(yaml_node)
    args = {}
    sig = signature(func)
    for name, param in sig.parameters.items(): #type: str, Parameter
        if hasattr(func, '__cfgMap__') and name in func.__cfgMap__:
            if isinstance(func.__cfgMap__[name], TransformCfg):
                expression = func.__cfgMap__[name].expression
            else:
                expression = func.__cfgMap__[name]
            if expression:
                val = expression.search(yaml_node)
                if val is None:
                    val = param.default
                elif isinstance(func.__cfgMap__[name], TransformArg):
                    val = func.__cfgMap__[name](val)
                args[name] = val
        else:
            val = yaml_node.get(name, param.default)
            if val != param.empty:
                args[name] = val
    return args

def configUnmapped(func, param: str):
    """
    Helper to determine if a parameter mapping was set to None.
    :param func: The function to check.
    :param param: The parameter name to check.
    :return: True if the parameter mapping was set to none.
    """
    return hasattr(func, '__cfgMap__') and param in func.__cfgMap__ and func.__cfgMap__[param] is None

# -- Command line argument mapping --

class PositionalArg(TransformArg):
    """
    Extends :class:`TransformArg` to allow mapping to positional command line arguments.
    """
    __slots__ = 'index', 'name', 'desc', 'default'
    def __init__(self, index: int, name: str = None, desc: str = None, xform = None):
        """
        Constructor.
        :param index: The 0-indexed position of the command line parameter.
        :param name: The name of the command line parameter to display in the help.
        :param desc: The description of the parameter to display in the help.
        :param xform: See :meth:`TransformArg.__init__`
        """
        self.index = index
        self.name = name # TODO use function param name if None
        self.desc = desc # TODO use function doc if None
        self.default = None
        super().__init__(xform)

    @property
    def optional(self):
        """
        Determines if a default value was specified in the function definition.
        Depends on @ArgMap to set the :attr:`default` attribute of this object.
        :return: True if a default value was set, false otherwise.
        """
        return self.default is not Parameter.empty

def ArgMap(*args, **kwargs):
    """
    Function decorator that specifies parameter mappings to command line parameters.
    The values of the arguments should either be a string with the command line parameter name,
    None to have configutator ignore the parameter when mapping, or a :class:`TransformArg` instance.
    Pass "_func='prefix'" as an argument to specify the prefix to use for the command line arguments.
    Gives the decorated function object an __argMap__ attribute.
    :param args: Positional arguments that coincide with the arguments of the function to decorate.
    :param kwargs: Keyword arguments that coincide with the arguments of the function to decorate. This will override anything conflicting with args.
    :return: A function that will add the specified mappings to the function passed to its single argument.
    """
    def wrap(func):
        sig = signature(func)
        nArgs = normaliseArgs(func, args, kwargs)
        if not hasattr(func, '__argMap__'):
            func.__argMap__ = {}
        if '_func' in nArgs:
            func.__argMap__['_func'] = nArgs['_func']
        for name, param in sig.parameters.items():
            if name in nArgs:
                if isinstance(nArgs[name], PositionalArg) and param.default is not param.empty:
                    nArgs[name].default = param.default
                func.__argMap__[name] = nArgs[name] or None

        return func
    return wrap

def mapArgs(optList: list, positionals: list, functions: list) -> dict:
    """
    Maps the values in optList and positionals to the parameters of the passed functions
    :param optList: A list of arguments produced by :func:`getopt.gnu_getopt`()
    :param positionals: A list of positional arguments produced by :func:`getopt.gnu_getopt`()
    :param functions: A list of functions to map the command line argument values to.
    :return: A dict keyed on the functions parameter names with the values found in optList and positionals.
    """
    args = {}
    pos = [] # Accumulate all positionals from all functions for later processing
    for f in functions:
        sig = signature(f)
        args[f] = {}
        for name, param in sig.parameters.items():
            positional = resolvePositional(f, name)
            if positional:
                pos.append((f, name, positional))
            else:
                argName = resolveArgName(f, name)
                if not argName: continue
                for opt, val in optList:
                    if opt == '--' + argName:
                        if hasattr(f, '__argMap__') and name in f.__argMap__ and isinstance(f.__argMap__[name], TransformArg):
                            val = f.__argMap__[name](val)
                        elif issubclass(getTrueAnnotationType(sig.parameters[name].annotation), bool):
                            val = strtobool(val or 'True')
                        elif sig.parameters[name].annotation is not Parameter.empty:
                            val = getTrueAnnotationType(sig.parameters[name].annotation)(val)
                        args[f][name] = val
    requiredCount = len({positional.index: True for f, name, positional in pos if not positional.optional})
    remaining = len(positionals) - requiredCount
    if remaining < 0:
        raise ValueError("Expected {} positional arguments, {} found.".format(requiredCount, len(positionals)))
    for i in range(len(positionals)):
        for f, name, positional in pos:
            if positional.index == i:
                if positional.optional and remaining:
                    remaining -= 1
                else:
                    continue
                args[f][name] = positional(positionals[i])
    return args

def resolvePositional(func, name) -> PositionalArg or None:
    """
    Determine if a function parameter has a specified positional mapping.
    :param func: The function to check.
    :param name: The parameter name to check.
    :return: The PositionalArg instance or None
    """
    if hasattr(func, '__argMap__') and name in func.__argMap__ and isinstance(func.__argMap__[name], PositionalArg):
        return func.__argMap__[name]
    else:
        return None

def resolveArgPrefix(function) -> str:
    """
    Resolve the command line prefix for a function.
    :param function: The function to resolve.
    :return: The value of the '_func' property set by @ArgMap or the function name if not set.
    """
    # Handle _func in argMap
    prefix = function.__name__ + ':'
    if hasattr(function, '__argMap__') and '_func' in function.__argMap__ and function.__argMap__['_func'] is not None:
        prefix = function.__argMap__['_func']
        if prefix != '':
            prefix += ':'
    return prefix

def resolveArgName(func, name) -> str:
    """
    Resolve the command line argument name for the specified function parameter.
    :param func: The function to resolve.
    :param name: The parameter name to resolve.
    :return: A string containing the fully resolved command line argument name.
    """
    # Prefix parameter with name if argMap unspecified
    if hasattr(func, '__argMap__'):
        if name in func.__argMap__:
            if func.__argMap__[name]:
                if isinstance(func.__argMap__[name], PositionalArg):
                    return func.__argMap__[name].name
                return func.__argMap__[name]
            else:
                return None
        elif '_func' in func.__argMap__:
            if func.__argMap__['_func'] is not None:
                return func.__argMap__['_func'] + ':' + name
            else:
                return name
        else:
            return name
    else:
        return func.__name__ + ':' + name

def argUnmapped(func, param: str) -> bool:
    """
    Helper to determine if a parameter mapping was set to None.
    :param func: The function to check.
    :param param: The parameter name to check.
    :return: True if the parameter mapping was set to none.
    """
    return hasattr(func, '__argMap__') and param in func.__argMap__ and func.__argMap__[param] is None

# -- TUI Builder --

def boolParam(param: Parameter, desc: str, layout: Widgets.Layout, maxWidth = None):
    layout.add_widget(Widgets.CheckBox(desc, param.name, param.name))

def textParam(param: Parameter, desc: str, layout: Widgets.Layout, maxWidth = None):
    layout.add_widget(Widgets.Text(name=param.name, label=param.name))
    if desc:
        lastI = 0
        for i in range(maxWidth or len(desc), len(desc), maxWidth or len(desc)):
            layout.add_widget(Widgets.Label(desc[lastI:i]))
            lastI = i
        layout.add_widget(Widgets.Divider(False))

widgetMap = {
    'Path': textParam,
    'PathOrNone': textParam,
    'str': textParam,
    'int': textParam,
    'bool': boolParam
}

def _configUI(screen, functions: list, yaml_node, call_name, title=''):
    Widgets.Frame.palette['edit_text'] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_CYAN)
    Widgets.Frame.palette['section_header'] = (Screen.COLOUR_GREEN, Screen.A_UNDERLINE, Screen.COLOUR_BLUE)

    windowWidth = screen.width * 2 // 3
    data = {}
    historyPath = os.path.expanduser('~/.configutator_history')
    if os.path.exists(historyPath):
        with open(historyPath, 'rb') as file:
            history = pickle.load(file)
            if call_name in history:
                data = history[call_name]
    window = Widgets.Frame(screen, screen.height * 2 // 3, windowWidth, title=title, data=data)
    scene = Scene([window])

    def saveHistory():
        history = {}
        if os.path.exists(historyPath):
            with open(historyPath, 'rb') as file:
                history = pickle.load(file)
        history[call_name] = window.data
        with open(historyPath, 'wb+') as file:
            pickle.dump(history, file)

    def _go():
        window.save()
        saveHistory()
        raise StopApplication('')
    def _close():
        window.save()
        saveHistory()
        raise StopApplication('')
    def _save():
        pass
    def _load():
        pass
    def inputHandler(event):
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            # Stop on ctrl+q or ctrl+x or esc
            if c in (17, 24, 27):
                _close()

    for f in functions:
        doc = getParamDoc(f)
        layout = Widgets.Layout([1])
        window.add_layout(layout)
        sig = signature(f)
        if len(functions) > 1:
            label = Widgets.Label(f.__name__+':')
            label.custom_colour = 'section_header'
            layout.add_widget(label)
        for name, param in sig.parameters.items(): #type: str, Parameter
            if param.annotation.__name__ in widgetMap:
                widgetMap[param.annotation.__name__](param, doc.get(name, ''), layout, windowWidth)
        layout.add_widget(Widgets.Divider(False))

    toolbar = Widgets.Layout([1,1,1,1])
    window.add_layout(toolbar)
    load_button = Widgets.Button('Load', _load)
    save_button = Widgets.Button('Save', _save)
    cancel_button = Widgets.Button('Cancel', _close)
    go_button = Widgets.Button('GO', _go)
    toolbar.add_widget(load_button, 0)
    toolbar.add_widget(save_button, 1)
    toolbar.add_widget(cancel_button, 2)
    toolbar.add_widget(go_button, 3)

    window.fix()
    screen.play([scene], unhandled_input=inputHandler)

# -- Loader --

def loadConfig(argv: list, functions: tuple, title='', positionalDoc: list=[], configParam='config', defaultConfig=None, configExpression = None, batchExpression=None) -> dict:
    if isinstance(configExpression, str):
        configExpression = jmespath.compile(configExpression)
    if isinstance(batchExpression, str):
        batchExpression = jmespath.compile(batchExpression)

    call_name = argv[0]
    argv = argv[1:]
    options = [configParam + '=', '{}:='.format(configParam), '{}:params:='.format(configParam), '{}:batch:='.format(configParam)]
    for f in functions:
        # Build command line argument list from function parameters
        sig = signature(f)
        for name, param in sig.parameters.items():
            name = resolveArgName(f, name)
            if not name: continue
            # If boolean, make parameter valueless
            if not ((issubclass(getTrueAnnotationType(param.annotation), bool) or isinstance(param.default, bool)) and param.default == False):
                name += '='
            options.append(name)
    optList, originalPositionals = gnu_getopt(argv, 'h', options)

    # Search for help switch in passed parameters
    for opt, val in optList:
        if opt == '-h':
            from sys import stderr
            import __main__
            headerString = ''
            positionalHelp = {} # type: dict[int, PositionalArg]
            helpString = ''
            try:
                if title:
                    headerString = "{}\tUse: {} [options] ".format(title, getfile(__main__))
            except TypeError:
                pass
            for f in functions:
                # Build command line argument option descriptions from function parameters
                sig = signature(f)
                if len(functions) > 1: helpString += "{}:\n".format(f.__name__)
                funcDocs = funcDocRegex.findall(getdoc(f))
                if len(funcDocs):
                    helpString += funcDocs[0] + '\n'
                doc = getParamDoc(f)
                for name, param in sig.parameters.items(): #type:str, Parameter
                    positional = resolvePositional(f, name)
                    if positional:
                        positionalHelp[positional.index] = positional
                    else:
                        argName = resolveArgName(f, name)
                        if not argName: continue
                        default = ''
                        if param.default != param.empty:
                            default = "[Default: {}]".format(param.default)
                        helpString += "  --{} - {} {}\n".format(argName, doc.get(name, ''), default)

            helpString += "General:\n  --{} - Path to configuration file. All other specified options override config. " \
                          "If no config file specified, all options without default must be specified.\n".format(configParam)
            if headerString:
                positionalNameString = ''
                positionalDocString = ''
                try:
                    for i in range(len(positionalHelp)):
                        positionalNameString += (" [{}]" if positionalHelp[i].optional else " {}").format(positionalHelp[i].name)
                        positionalDocString += "{} - {}\n".format(positionalHelp[i].name, positionalHelp[i].desc)
                    stderr.write(headerString + positionalNameString + '\n' + positionalDocString + helpString)
                except KeyError:
                    raise ValueError("Non-contiguous positional parameter index: {}".format(i))
            else:
                stderr.write(helpString)
            exit()

    # Handle config path overrides
    for f in functions:
        for name, param in signature(f).parameters.items():
            prefix = '--' + resolveArgPrefix(f)
            for opt, val in optList:
                if opt == prefix:
                    ConfigMap(_func=jmespath.compile(val))(f)
                elif opt == prefix + name + ':':
                    ConfigMap(**{name: jmespath.compile(val)})(f)

    config = None
    # Search for configParam in passed parameters
    for opt, val in optList:
        if opt == '--' + configParam:
            if not (os.path.isfile(val) and os.access(val, os.R_OK)):
                raise FileNotFoundError("The config path was not found: {}".format(val))
            for o, v in optList:
                if o == '--{}:'.format(configParam):
                    configExpression = jmespath.compile(v)
                elif o == '--{}:batch:'.format(configParam):
                    batchExpression = jmespath.compile(v)
            config = val

    args = mapArgs(optList, originalPositionals, functions)
    if config:
        cfgs = ruamel.yaml.load_all(open(config), YAMLLoader)
        for cfg in cfgs:
            if configExpression:
                tmp = configExpression.search(cfg)
                if tmp != None:
                    cfg = tmp
            if batchExpression:
                jobs = batchExpression.search(cfg)
                if jobs == None:
                    jobs = [cfg]
            else:
                jobs = [cfg]
            for job in jobs:
                argMap = {}
                for f in functions:
                    argMap[f] = mapConfig(f, job)
                for f, m in args.items():
                    if f not in argMap:
                        argMap[f] = {}
                    argMap[f].update(m)
                for f in functions:
                    validate(f, argMap[f])
                #TODO os.fork() to parallelize jobs
                yield argMap
        return

    if len(argv):
        # If parameters were passed, skip TUI
        yield args
        return
    else:
        # No parameters were passed, load TUI
        cfg = None
        if defaultConfig is not None:
            cfg = ruamel.yaml.load(defaultConfig, YAMLLoader)
        Screen.wrapper(_configUI, arguments=(functions, cfg, call_name, title))
