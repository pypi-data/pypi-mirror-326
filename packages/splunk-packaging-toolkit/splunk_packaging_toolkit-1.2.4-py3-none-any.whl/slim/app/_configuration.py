# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

""" app_configuration module

The app_configuration_spec module defines this class hierarchy:

.. code-block::
    AppConfiguration(ObjectView)
    |
    └-> (attribute, files: AppConfigurationFile* )*
                    |
                    ├-> filename: string
                    |
                    └-> stanzas: (
                            name: string,
                            AppConfigurationStanza(NamedObject) )*
                            |
                            ├-> placement: AppConfigurationPlacement
                            |
                            ├-> position: FilePosition
                            |
                            └-> settings: (
                                    name: string,
                                    AppConfigurationSetting)*
                                    |
                                    ├-> name: string
                                    |
                                    ├-> value: string
                                    |
                                    ├-> position: FilePosition
                                    |
                                    └-> placement: AppConfigurationPlacement
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import object
from collections import OrderedDict
from glob import glob
from itertools import chain
from os import path

import io

from . _configuration_validator import AppConfigurationValidator
from . _internal import FileBuffer, NamedObject, ObjectView
from .. utils import SlimLogger, encode_string
from .. utils.internal import string


class AppConfiguration(object):

    def __init__(self, app_root):
        """ Create an AppConfiguration object that holds the results from parse conf.

        """
        self._app_root = app_root
        self._files = None

    # region Special methods

    def __repr__(self):
        return self.__class__.__name__ + '(app_root=' + repr(self._app_root) + ')'

    # endregion

    # region Accessors

    @property
    def app_root(self):
        return self._app_root

    def files(self):
        files = self._files
        return (files[name] for name in files)

    def get(self, file, stanza=None, setting=None):  # pylint: disable=redefined-builtin
        if stanza is None and setting is not None:
            raise ValueError('Expected setting to be None because stanza is None')
        try:
            file = self._files[file]
        except KeyError:
            value = None
        else:
            value = file if stanza is None else file.get(stanza, setting)
        return value

    def get_value(self, file, stanza, setting, default=None):  # pylint: disable=redefined-builtin
        try:
            file = self._files[file]
        except KeyError:
            value = _default_value(setting, default)[0]
        else:
            value = file.get_value(stanza, setting, default)
        return value

    def has(self, file, stanza=None, setting=None):  # pylint: disable=redefined-builtin
        if stanza is None and setting is not None:
            raise ValueError('Expected setting to be None because stanza is None')
        try:
            file = self._files[file]
        except KeyError:
            value = False
        else:
            value = True if stanza is None else file.has(stanza, setting)
        return value

    # endregion

    # region Methods

    @classmethod
    def load(cls, app_root):
        # TODO: find the right place to validate that the app_root is a directory that contains an app  (here?)
        configuration = cls(app_root)
        configuration._load()  # pylint: disable=protected-access
        return configuration

    def save(self, file, indent=False):  # pylint: disable=redefined-builtin
        if isinstance(file, string):
            with io.open(file, encoding='utf-8', mode='w', newline='') as ostream:
                self._save(ostream, indent)
            return
        self._save(file, indent)

    def to_dict(self):
        files = self._files
        value = OrderedDict(((name, files[name]) for name in files))  # copying protects our internals
        return value

    # endregion

    # region Protected

    def _load(self):

        app_root = self._app_root
        basename = path.basename
        isdir = path.isdir
        join = path.join

        directory_names = (n for n in (join(app_root, n) for n in ('default', 'local')) if isdir(n))
        configurations = OrderedDict()
        end = -len('.conf')

        for filename in chain.from_iterable(sorted(glob(join(d, '*.conf'))) for d in directory_names):
            name = basename(filename)[:end]
            try:
                filenames = configurations[name]
            except KeyError:
                filenames = [filename]
            else:
                filenames.append(filename)
            configurations[name] = filenames

        files = OrderedDict()

        for name in configurations:
            configuration_file = AppConfigurationFile(name)
            with AppConfigurationValidator(name, app_root) as validator:
                for filename in configurations[name]:
                    configuration_file.load(filename, validator)
            files[name] = configuration_file

        self._files = files

    def _save(self, ostream, indent):
        iterencode = ObjectView.iterencode_indent if indent is True else ObjectView.iterencode
        for chunk in iterencode(self):
            ostream.write(string(chunk))

    # endregion
    pass  # pylint: disable=unnecessary-pass


class AppConfigurationFile(NamedObject):

    def __init__(self, name):
        NamedObject.__init__(self, name)
        self._sections = OrderedDict()
        self._stanzas = OrderedDict()

    # region Special methods

    def __repr__(self):
        return self.__class__.__name__ + '(name=' + repr(self._name) + 'stanzas=' + repr(self._stanzas) + ')'

    def __str__(self):
        return encode_string(self._name)

    # endregion

    # region Accessors

    def get(self, stanza, setting=None):
        try:
            stanza = self._stanzas[stanza]
        except KeyError:
            value = None
        else:
            value = stanza if setting is None else stanza.get(setting)
        return value

    def get_value(self, stanza, setting, default=None):
        try:
            stanza = self._stanzas[stanza]
        except KeyError:
            value = _default_value(setting, default)[0]
        else:
            value = stanza.get_value(setting, default)
        return value

    def has(self, stanza, setting=None):
        try:
            stanza = self._stanzas[stanza]
        except KeyError:
            value = False
        else:
            value = True if setting is None else stanza.has(setting)
        return value

    def sections(self):
        sections = self._sections
        return (sections[name] for name in sections)

    def stanzas(self):
        stanzas = self._stanzas
        return (stanzas[name] for name in stanzas)

    # endregion

    # region Methods

    def load(self, filename, validator):

        section = AppConfigurationFile.Section.load(filename, validator)
        stanzas = self._stanzas

        for section_stanza in section.stanzas():
            name = section_stanza.name
            try:
                stanza = stanzas[name]
            except KeyError:
                stanza = AppConfigurationStanza(name)
                stanzas[name] = stanza
            stanza.add(section_stanza)

        self._sections[filename] = section

    def to_dict(self):
        sections = self._sections
        return OrderedDict(((name, sections[name]) for name in sections))  # copying protects our internals

    # endregion

    class Section(object):

        def __init__(self, file_buffer):
            self._file_buffer = file_buffer

        # region Special methods

        def __repr__(self):
            name, stanzas = repr(self.name), repr(self._file_buffer.stanzas)
            return self.__class__.__name__ + '(name=' + name + ', stanzas=' + stanzas + ')'

        def __str__(self):
            return encode_string(self.name)

        # endregion

        # region Properties

        @property
        def name(self):
            return self._file_buffer.filename

        # endregion

        # region Accessors

        def get(self, name):
            return self._file_buffer.setting.get(name)

        def stanzas(self):
            stanzas = self._file_buffer.stanzas
            return (stanzas[name] for name in stanzas)

        # endregion

        # region Methods

        @classmethod
        def load(cls, filename, validator):
            file_buffer = _AppConfigurationFileBuffer(filename)
            file_buffer.load(validator=validator)
            return cls(file_buffer)

        def save(self, filename=None):
            self._file_buffer.save(filename)

        def to_dict(self):
            return OrderedDict(((stanza.name, stanza) for stanza in self.stanzas()))  # copying protects our internals

        # endregion
        pass  # pylint: disable=unnecessary-pass

    Section.__name__ = str('AppConfigurationFile.Section')


class AppConfigurationSetting(NamedObject):

    def __init__(self, name):
        NamedObject.__init__(self, name)
        self._sections = OrderedDict()
        self._setting = None

    # region Special methods

    def __eq__(self, other):
        return isinstance(other, AppConfigurationSetting) and self.value == other.value

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return not (self < other or self == other)

    def __le__(self, other):
        return self < other or self == other

    def __lt__(self, other):
        return isinstance(other, AppConfigurationSetting) and self.value < other.value

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        name, placement, position = repr(self._name), repr(self.placement), repr(self.position)
        return self.__class__.__name__ + '(name=' + name + ', placement=' + placement + ', position=' + position + ')'

    def __str__(self):
        return self._setting.__str__()

    # endregion

    # region Properties

    @property
    def placement(self):
        return self._setting.placement

    @property
    def position(self):
        return self._setting.position

    @property
    def value(self):
        return self._setting.value

    # endregion

    # region Methods

    def add(self, section):
        self._sections[section.name] = self._setting = section  # last-in section holds the value of this setting

    def to_dict(self):
        return self._setting.to_dict()

    # endregion

    class Section(NamedObject):

        def __init__(self, name, value, position, placement=None):

            NamedObject.__init__(self, name)
            self._placement = placement
            self._position = position
            self._value = '' if value is None else value.strip()

        # region Special methods

        def __repr__(self):
            property_names = self._property_names
            arguments = (n + '=' + repr(getattr(self, property_names[n])) for n in property_names)
            return self.__class__.__name__ + '(' + ', '.join(arguments) + ')'

        def __str__(self):
            return self._name + ' = ' + string(self._value).replace('\n', '\\\n')

        # endregion

        # region Properties

        @property
        def position(self):
            return self._position

        @property
        def placement(self):
            return self._placement

        @property
        def value(self):
            return self._value

        # endregion

        # region Methods

        def to_dict(self):
            return OrderedDict((('value', self._value), ('placement', self._placement), ('line', self._position.line)))

        # endregion

        # region Protected

        _property_names = OrderedDict(((name, '_' + name) for name in ('name', 'value', 'placement', 'position')))

        # endregion
        pass  # pylint: disable=unnecessary-pass

    Section.__name__ = str('AppConfigurationSetting.Section')


class AppConfigurationStanza(NamedObject):

    def __init__(self, name):
        NamedObject.__init__(self, name)
        self._sections = OrderedDict()
        self._settings = OrderedDict()
        self._placement = None

    # region Special methods

    def __repr__(self):
        return self.__class__.__name__ + '(name=' + repr(self._name) + ', settings=' + repr(self._settings) + ')'

    def __str__(self):
        return '[' + self._name.replace('\n', '\\n') + ']'

    # endregion

    # region Properties

    @property
    def placement(self):
        return self._placement

    # endregion

    # region Accessors

    def add(self, section):

        settings = self._settings

        for section_setting in section.settings():
            try:
                setting = settings[section_setting.name]
            except KeyError:
                setting = AppConfigurationSetting(section_setting.name)
                settings[setting.name] = setting
            setting.add(section_setting)

        assert self._placement is None or self._placement == section.placement
        self._sections[section.position.file] = section
        self._placement = section.placement

    def get(self, setting):
        get = self._settings.get
        if isinstance(setting, tuple):
            item = tuple((get(name) for name in setting))
        else:
            item = get(setting)
        return item

    def get_value(self, setting, default=None):

        default, is_tuple = _default_value(setting, default)

        if is_tuple is True:
            value = [None] * len(setting)
            for i, name in enumerate(setting):
                try:
                    value[i] = self._settings[name].value
                except KeyError:
                    value[i] = default[i]
            value = tuple(value)
        else:
            name = setting
            try:
                value = self._settings[name].value
            except KeyError:
                value = default

        return value

    def has(self, setting):
        return setting in self._settings

    def settings(self):
        settings = self._settings
        return (settings[name] for name in settings)

    # endregion

    # region Methods

    def to_dict(self):
        settings = self._settings
        OrderedDict((name, settings[name]) for name in self._settings)  # copying protects our internals

    # endregion

    class Section(NamedObject):

        def __init__(self, name, placement, position):
            NamedObject.__init__(self, name)
            self._settings = OrderedDict()
            self._placement = placement
            self._position = position

        # region Special methods

        def __repr__(self):
            return self.__class__.__name__ + '(name=' + repr(self._name) + ', position=' + repr(self._position) + ')'

        def __str__(self):
            return '[' + self._name.replace('\n', '\\n') + ']'

        # endregion

        # region Properties

        @property
        def placement(self):
            return self._placement

        @property
        def position(self):
            return self._position

        # endregion

        # region Methods

        def add(self, setting):
            self._settings[setting.name] = setting

        def get(self, name):
            return self._settings.get(name)

        def get_value(self, name, default=None):
            try:
                setting = self._settings[name]
            except KeyError:
                value = default
            else:
                value = setting.name
            return value

        def settings(self):
            settings = self._settings
            return (settings[name] for name in settings)

        def to_dict(self):
            return OrderedDict((setting.name, setting) for setting in self.settings())  # copying protects our internals

        # endregion
        pass  # pylint: disable=unnecessary-pass

    Section.__name__ = str('AppConfigurationStanza.Section')


# region Protected

def _default_value(setting, default):
    if not isinstance(setting, tuple):
        return default, False
    if default is None:
        return (None,) * len(setting), True
    if not isinstance(default, tuple):
        raise TypeError('Expected default: tuple, not default: ', type(setting).__name__)
    if len(default) != len(setting):
        raise ValueError('Expected len(default) == len(setting)')
    return tuple(default), True


class _AppConfigurationFileBuffer(FileBuffer):

    def __init__(self, filename):
        FileBuffer.__init__(self, filename)
        self._stanzas = None

    # region Properties

    @property
    def stanzas(self):
        return self._stanzas

    # endregion

    # region Protected

    def _load(self, reader, **kwargs):
        """ Loads or reloads the conf file associated with the current Buffer

        """
        match_assignment_statement = self._match_assignment_statement
        skip_whitespace = self._skip_whitespace
        self._stanzas = stanzas = OrderedDict()
        validator = kwargs['validator']

        current_stanza = None
        validate_setting = None

        for line in reader:
            try:
                match = skip_whitespace(line)
                start = match.end()
                if start >= len(line):
                    # blank line
                    item = '\n'
                    start = 0
                elif line[start] in ';#':
                    # comment
                    item = line[start:]
                else:
                    line = reader.read_continuation(line)
                    if line[start] == '[':
                        # stanza where namesakes are merged (by way of the call to stanzas.setdefault)
                        item = self._parse_stanza(line, start, reader, validator)
                        validate_setting = validator.get(item)
                        item = current_stanza = stanzas.setdefault(item.name, item)
                    else:
                        if current_stanza is None:
                            # settings before a stanza get put into the [default] stanza
                            current_stanza = AppConfigurationStanza.Section(
                                'default', validator.get_placement('default'), reader.position
                            )
                            validate_setting = validator.get(current_stanza)
                            stanzas['default'] = current_stanza
                        # setting where namesakes are replaced
                        match = match_assignment_statement(line, start)
                        if match is None:
                            text = encode_string(line.strip())
                            raise self._Error('Expected a setting assignment, not ' + text)
                        item = AppConfigurationSetting.Section(
                            name=match.group(1), value=match.group(2), position=reader.position,
                            placement=current_stanza.placement)
                        current_stanza.add(item)
                        validate_setting(item)
                self._append(item, reader.position, indentation=start)
            except self._Error as error:
                SlimLogger.error(reader.position, ': ', error)

    def _parse_stanza(self, line, start, reader, validator):

        start += 1
        match = self._search_right_square_bracket(line, start)

        if match is None:
            SlimLogger.warning(reader.position, ': missing terminating right square bracket at end of stanza header')
            end = -1
        else:
            end = match.start()

        name = line[start:end]
        placement = validator.get_placement(name)
        return AppConfigurationStanza.Section(name, placement, reader.position)

    # endregion
    pass  # pylint: disable=unnecessary-pass

# endregion
