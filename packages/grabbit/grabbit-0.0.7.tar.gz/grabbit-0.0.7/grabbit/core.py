import json
import os
import re
from collections import defaultdict, OrderedDict, namedtuple
from grabbit.external import six, inflect
from grabbit.utils import natural_sort
from os.path import join, basename, dirname, abspath, split
from functools import partial


__all__ = ['File', 'Entity', 'Layout']


class File(object):

    def __init__(self, filename):
        """
        Represents a single file.
        """
        self.path = filename
        self.filename = basename(self.path)
        self.dirname = dirname(self.path)
        self.entities = {}

    def _matches(self, entities=None, extensions=None, regex_search=False):
        """
        Checks whether the file matches all of the passed entities and
        extensions.
        Args:
            entities (dict): A dictionary of entity names -> regex
                patterns.
            extensions (str, list): One or more file extensions to allow.
            regex_search (bool): Whether to require exact match (False) or
                regex
                search (True) when comparing the query string to each entity.
        Returns:
            True if _all_ entities and extensions match; False otherwise.
        """
        if extensions is not None:
            if isinstance(extensions, six.string_types):
                extensions = [extensions]
            extensions = '(' + '|'.join(extensions) + ')$'
            if re.search(extensions, self.path) is None:
                return False
        if entities is not None:
            for name, val in entities.items():
                patt = '%s' % val
                if isinstance(val, (int, float)):
                    # allow for leading zeros if a number was specified
                    # regardless of regex_search
                    patt = '0*' + patt
                if not regex_search:
                    patt = '^%s$' % patt
                if name not in self.entities or \
                        re.search(patt, self.entities[name]) is None:
                    return False
        return True

    def as_named_tuple(self):
        """
        Returns the File as a named tuple. The full path plus all entity
        key/value pairs are returned as attributes.
        """
        _File = namedtuple('File', 'filename ' + ' '.join(self.entities.keys()))
        return _File(filename=self.path, **self.entities)


class Entity(object):

    def __init__(self, name, pattern, mandatory=False, directory=None,
                 **kwargs):
        """
        Represents a single entity defined in the JSON config.
        Args:
            name (str): The name of the entity (e.g., 'subject', 'run', etc.)
            pattern (str): A regex pattern used to match against file names.
                Must define at least one group, and only the first group is
                kept as the match.
            mandatory (bool): If True, every File _must_ match this entity.
            kwargs (dict): Additional keyword arguments.
        """
        self.name = name
        self.pattern = pattern
        self.mandatory = mandatory
        self.directory = directory
        self.files = {}
        self.regex = re.compile(pattern)

    def __iter__(self):
        for i in self.unique():
            yield(i)

    def matches(self, f):
        """
        Run a regex search against the passed file and update the entity/file
        mappings.
        Args:
            f (File): The File instance to match against.
        """
        m = self.regex.search(f.path)
        if m is not None:
            val = m.group(1)
            f.entities[self.name] = val

    def add_file(self, filename, value):
        """ Adds the specified filename to tracking. """
        self.files[filename] = value

    def unique(self):
        """ Returns all unique values/levels for the current entity. """
        return list(set(self.files.values()))

    def count(self, files=False):
        """ Returns a count of unique values or files.
        Args:
            files (bool): When True, counts all files mapped to the Entity.
                When False, counts all unique values.
        Returns: an int.
        """
        return len(self.files) if files else len(self.unique())


class Layout(object):

    def __init__(self, path, config=None, dynamic_getters=False,
                 absolute_paths=True, regex_search=False, exclude_dir=None):
        """
        A container for all the files and metadata found at the specified path.
        Args:
            path (str): The root path of the layout.
            config (str): The path to the JSON config file
                that defines the entities and paths for the current layout.
            dynamic_getters (bool): If True, a get_{entity_name}() method will
                be dynamically added to the Layout every time a new Entity is
                created. This is implemented by creating a partial function of
                the get() function that sets the target argument to the
                entity name.
            absolute_paths (bool): If True, grabbit uses absolute file paths
                everywhere (including when returning query results). If False,
                the input path will determine the behavior (i.e., relative if
                a relative path was passed, absolute if an absolute path was
                passed).
            regex_search (bool): Whether to require exact matching (True)
                or regex search (False, default) when comparing the query
                string to each entity in .get() calls. This sets a default for
                the instance, but can be overridden in individual .get()
                requests.
            exclude_dir (str): Regex by which to exclude directories (and their
                children) from indexing.
        """

        self.root = abspath(path) if absolute_paths else path
        self.entities = OrderedDict()
        self.files = {}
        self.mandatory = set()
        self.dynamic_getters = dynamic_getters
        self.regex_search = regex_search
        self.exclude_dir = exclude_dir

        if config is not None:
            self._load_config(config)

    def _load_config(self, config):
        if isinstance(config, six.string_types):
            config = json.load(open(config, 'r'))

        for e in config['entities']:
            self.add_entity(**e)

        self.index()

    def _validate_file(self, f):
        ''' Override this in subclasses to provide additional file validation.
        Will be called the first time each file is read in; if False is
        returned, the file will be ignored and dropped from the layout. '''
        return True

    def index(self):

        # Reset indexes
        self.files = {}
        for ent in self.entities.values():
            ent.files = {}

        # Loop over all files
        for root, directories, filenames in os.walk(self.root, topdown=True):

            # Exclude directories from further search if they match exclude regex
            if self.exclude_dir is not None:
                directories[:] = [d for d in directories if not re.match(self.exclude_dir, d)]

            for f in filenames:
                f = File(join(root, f))
                if not self._validate_file(f):
                    continue
                for e in self.entities.values():
                    e.matches(f)
                fe = f.entities.keys()
                # Only keep Files that match at least one Entity, and all
                # mandatory Entities
                if fe and not (self.mandatory - set(fe)):
                    self.files[f.path] = f
                    # Bind the File to all of the matching entities
                    for ent, val in f.entities.items():
                        self.entities[ent].add_file(f.path, val)

    def add_entity(self, **kwargs):
                # Set up the entities we need to track
            ent = Entity(**kwargs)
            if ent.mandatory:
                self.mandatory.add(ent.name)
            if ent.directory is not None:
                ent.directory = ent.directory.replace('{{root}}', self.root)
            self.entities[ent.name] = ent
            if self.dynamic_getters:
                func = partial(getattr(self, 'get'), target=ent.name,
                               return_type='id')
                func_name = inflect.engine().plural(ent.name)
                setattr(self, 'get_%s' % func_name, func)

    def get(self, return_type='tuple', target=None, extensions=None,
            regex_search=None, **kwargs):
        """
        Retrieve files and/or metadata from the current Layout.
        Args:
            return_type (str): Type of result to return. Valid values:
                'tuple': returns a list of namedtuples containing file name as
                    well as attribute/value pairs for all named entities.
                'file': returns a list of matching filenames.
                'dir': returns a list of directories.
                'id': returns a list of unique IDs. Must be used together with
                    a valid target.
            target (str): The name of the target entity to get results for
                (if return_type is 'dir' or 'id').
            extensions (str, list): One or more file extensions to filter on.
                Files with any other extensions will be excluded.
            regex_search (bool or None): Whether to require exact matching
                (False) or regex search (True) when comparing the query string
                to each entity. If None (default), uses the value found in
                self.
            kwargs (dict): Any optional key/values to filter the entities on.
                Keys are entity names, values are regexes to filter on. For
                example, passing filter={ 'subject': 'sub-[12]'} would return
                only files that match the first two subjects.

        Returns:
            A named tuple (default) or a list (see return_type for details).
        """
        if regex_search is None:
            regex_search = self.regex_search

        result = []
        filters = {}
        filters.update(kwargs)
        for filename, file in self.files.items():
            if not file._matches(filters, extensions, regex_search):
                continue
            result.append(file)

        if return_type == 'file':
            return natural_sort([f.path for f in result])

        if return_type == 'tuple':
            result = [r.as_named_tuple() for r in result]
            return natural_sort(result, field='filename')

        else:
            if target is None:
                raise ValueError('If return_type is "id" or "dir", a valid '
                                 'target entity must also be specified.')
            result = [x for x in result if target in x.entities]

            if return_type == 'id':
                result = list(set([x.entities[target] for x in result]))
                return natural_sort(result)

            elif return_type == 'dir':
                template = self.entities[target].directory
                if template is None:
                    raise ValueError('Return type set to directory, but no '
                                     'directory template is defined for the '
                                     'target entity (\"%s\").' % target)
                # Construct regex search pattern from target directory template
                to_rep = re.findall('\{(.*?)\}', template)
                for ent in to_rep:
                    patt = self.entities[ent].pattern
                    template = template.replace('{%s}' % ent, patt)
                template += '[^\%s]*$' % os.path.sep
                matches = [f.dirname for f in self.files.values() \
                           if re.search(template, f.dirname)]
                return natural_sort(list(set(matches)))

            else:
                raise ValueError("Invalid return_type specified (must be one "
                                 "of 'tuple', 'file', 'id', or 'dir'.")

    def unique(self, entity):
        """
        Return a list of unique values for the named entity.
        Args:
            entity (str): The name of the entity to retrieve unique values of.
        """
        return self.entities[entity].unique()

    def count(self, entity, files=False):
        """
        Return the count of unique values or files for the named entity.
        Args:
            entity (str): The name of the entity.
            files (bool): If True, counts the number of filenames that contain
                at least one value of the entity, rather than the number of
                unique values of the entity.
        """
        return self.entities[entity].count(files)

    def as_data_frame(self, **kwargs):
        """
        Return information for all Files tracked in the Layout as a pandas
        DataFrame.
        args:
            kwargs: Optional keyword arguments passed on to get(). This allows
                one to easily select only a subset of files for export.
        Returns:
            A pandas DataFrame, where each row is a file, and each column is
                a tracked entity. NaNs are injected whenever a file has no
                value for a given attribute.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("What are you doing trying to export a Layout "
                              "as a pandas DataFrame when you don't have "
                              "pandas installed? Eh? Eh?")
        if kwargs:
            files = self.get(return_type='file', **kwargs)
        else:
            files = self.files.values()
        data = pd.DataFrame.from_records([f.entities for f in files])
        data.insert(0, 'path', [f.path for f in files])
        return data

    def get_nearest(self, path, return_type='file', strict=True, all_=False,
                    ignore_strict_entities=None, **kwargs):
        ''' Walk up the file tree from the specified path and return the
        nearest matching file(s).
        Args:
            path (str): The file to search from.
            return_type (str): What to return; must be one of 'file' (default)
                or 'tuple'.
            strict (bool): When True, all entities present in both the input
                path and the target file(s) must match perfectly. When False,
                files will be ordered by the number of matching entities, and
                partial matches will be allowed.
            all_ (bool): When True, returns all matching files. When False
                (default), only returns the first match.
            ignore_strict_entities (list): Optional list of entities to
                exclude from strict matching when strict is True. This allows
                one to search, e.g., for files of a different type while
                matching all other entities perfectly by passing
                ignore_strict_entities=['type'].
            kwargs: Optional keywords to pass on to .get().
        '''

        entities = {}
        for name, ent in self.entities.items():
            m = ent.regex.search(path)
            if m:
                entities[name] = m.group(1)

        # Remove any entities we want to ignore when strict matching is on
        if strict and ignore_strict_entities is not None:
            for k in ignore_strict_entities:
                entities.pop(k, None)

        results = self.get(return_type='file', **kwargs)

        folders = defaultdict(list)

        for filename in results:
            f = self.files[filename]
            folders[f.dirname].append(f)

        def count_matches(f):
            keys = set(entities.keys()) & set(f.entities.keys())
            shared = len(keys)
            return [shared, sum([entities[k] == f.entities[k] for k in keys])]

        matches = []

        while True:
            if path in folders and folders[path]:

                # Sort by number of matching entities. Also store number of
                # common entities, for filtering when strict=True.
                num_ents = [[f] + count_matches(f) for f in folders[path]]
                # Filter out imperfect matches (i.e., where number of common
                # entities does not equal number of matching entities).
                if strict:
                    num_ents = [f for f in num_ents if f[1] == f[2]]
                num_ents.sort(key=lambda x: x[2], reverse=True)

                if num_ents:
                    matches.append(num_ents[0][0])

                if not all_:
                    break
            try:
                _path, _ = split(path)
                if _path == path:
                    break
                path = _path
            except:
                break

        matches = [m.path if return_type == 'file' else m.as_named_tuple()
                   for m in matches]
        return matches if all_ else matches[0] if matches else None
