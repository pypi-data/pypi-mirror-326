import os
import json

from opencos import util
from opencos.util import debug, info, warning, error


_include_iteration_max_depth = 128 # Depth to look for nested included files.
_remove_DEPS_yml_defines = [
    'OC_SEED',
    'OC_ROOT',
]


def json_paths_to_jsonl(json_file_paths:list, output_json_path:str,
                        assert_json_types=[dict]) -> None:
    '''Given a list of .json filepath strs, save a single .jsonl (newline separated json(s)).

    errors if one of json_file_paths content's type is not in assert_json_types
    (assert_json_types can be empty list to avoid check).
    '''

    if len(json_file_paths) == 0:
        error(f'{json_file_paths=} cannot be empty list')


    output_json_dir = os.path.split(output_json_path)[0]
    util.safe_mkdir(output_json_dir)

    with open(output_json_path, 'w') as outf:

        # jsonl is every line of the file is a json.
        for json_file_path in json_file_paths:
            with open(json_file_path) as f:
                data = json.load(f)
                if len(assert_json_types) > 0 and type(data) not in assert_json_types:
                    error(f'{json_file_path=} JSON data is not a Table (py dict) {type(data)=}')
                json.dump(data, outf)
                outf.write('\n')
        info(f'Wrote {len(json_file_paths)} tests to {output_json_path=}')


def json_paths_to_single_json(json_file_paths:list, output_json_path:str,
                              assert_json_types=[dict]) -> None:
    '''Given a list of .json filepath strs, save a single .json with key 'tests' and a list.

    errors if one of json_file_paths content's type is not in assert_json_types
    (assert_json_types can be empty list to avoid check).
    '''

    if len(json_file_paths) == 0:
        error(f'{json_file_paths=} cannot be empty list')


    output_json_dir = os.path.split(output_json_path)[0]
    util.safe_mkdir(output_json_dir)

    with open(output_json_path, 'w') as outf:

        out_json_data = {
            'tests': list(),
        }
        for json_file_path in json_file_paths:
            with open(json_file_path) as f:
                data = json.load(f)
                if len(assert_json_types) > 0 and type(data) not in assert_json_types:
                    error(f'{json_file_path=} JSON data is not a Table (py dict) {type(data)=}')
                out_json_data['tests'].append(data)
        json.dump(out_json_data, outf)
        outf.write('\n')
        info(f'Wrote {len(json_file_paths)} tests {output_json_path=}')


def find_sv_included_files_within_file(filename:str,
                                       known_incdir_paths:list,
                                       warnings:bool=True,
                                       modify_files_and_save_to_path=None,
                                       unmodified_files_link_to_path=None) -> list:
    '''Given a filename (full path) and a list of known incdir paths, returns
    a list of included files (full path).

    (Optional) modify_files_and_save_to_path (str: directory/path) if you wish
    to strip all path information on the `include "(path)" for example:
      `include "foo.svh" -- no modifications
      `include "../bar.svh" -- is modified to become `include "bar.svh"
    (Optional) unmodified_files_link_to_path (str: directory/path) if you wish
    to symlink unmodified files to this path.
    '''

    found_included_files = set()

    assert any(filename.endswith(x) for x in ['.v', '.sv', '.vh', '.svh']), \
        f'{filename=} does not have a supported extension, refusing to parse it'
    assert os.path.exists(filename), f'{filename=} does not exist'

    modified_lines = dict() # {linenum (int): line (str, modified line value), ...}

    filename_no_path = os.path.split(filename)[1]

    debug(f'export_helper: {filename=} {modify_files_and_save_to_path=} {unmodified_files_link_to_path=}')

    with open(filename) as f:

        for linenum, line in enumerate(f.readlines()):
            line_modified = False

            if '`include' in line:
                # strip comments on line, in case someone has: // `include "lib/foo.svh"
                # we can't handle /* comments */ on a line like this.
                assert '/*' not in line
                parts = line.split("//")
                words = parts[0].split() # only use what's on the left of the comments
                prev_word_is_tick_include = False
                for iter,word in enumerate(words):
                    word = word.rstrip('\n')
                    if word == '`include':
                        # don't print this word, wait until next word
                        prev_word_is_tick_include = True
                    elif prev_word_is_tick_include:
                        assert word.startswith('"')
                        assert word.endswith('"')
                        prev_word_is_tick_include = False
                        include_fname = word[1:-1] # trim " at start and end

                        # strip the path information and keep track that
                        # we would like to modify this line of filename
                        if modify_files_and_save_to_path:
                            include_fname_no_path = os.path.split(include_fname)[1]
                            if include_fname != include_fname_no_path:
                                words[iter] = '"' + include_fname_no_path + '"'
                                line_modified = True

                        if include_fname not in found_included_files:
                            # this has path information, perhaps relative, perhaps absolute, or
                            # perhaps relative to any of the +incdir+ paths. Figure that out later.
                            found_included_files.add(include_fname)

                if line_modified:
                    modified_lines[linenum] = ' '.join(words)

    debug(f'export_helper: {filename=} {modified_lines=}')
    # Optionally write out modified files (flatten the path information
    # on `include "../bar.svh" )
    if len(modified_lines) > 0 and modify_files_and_save_to_path:
        dst = os.path.join(modify_files_and_save_to_path, filename_no_path)
        if not os.path.exists(dst):
            with open(filename) as f, open(dst, 'w') as outf:
                for linenum, line in enumerate(f.readlines()):
                    if linenum in modified_lines:
                        new_line = modified_lines[linenum]
                        outf.write(new_line + '\n')
                        debug(f'export_helper: Modified {filename=} as {dst=}: {linenum=} {new_line=}')
                    else:
                        outf.write(line)

    # Optionally soft-link unmodified files to some path?
    if len(modified_lines) == 0 and unmodified_files_link_to_path:
        if os.path.isdir(unmodified_files_link_to_path):
            dst = os.path.join(unmodified_files_link_to_path, filename_no_path)
            if not os.path.exists(dst):
                debug(f'export_helper: Linked {filename=} to {dst=}')
                os.symlink(src=filename, dst=dst)


    # Back to the list found_included_files that we observed within our filename, we
    # still need to return all the included files.
    ret = list()
    for fname in found_included_files:
        # Does this file exist, using our known_incdir_paths?
        found = False
        for some_dir in known_incdir_paths:
            try_file_path = os.path.abspath(os.path.join(some_dir, fname))
            if os.path.exists(try_file_path):
                if try_file_path not in ret:
                    ret.append(try_file_path)
                    found = True
                    debug(f'export_helper: Include observed in {filename=} will use {try_file_path=} for export')
                    break # we can only match one possible file out of N possible incdir paths.


        if not found and warnings:
            # file doesn't exist in any included directory, we only warn here b/c
            # it will eventually fail compile.
            include_fname = fname
            warning( f'export_helper: {include_fname=} does not exist in any of {known_incdir_paths=},' \
                     + f'was included within source files: {filename=}'
                    )

    return ret



def get_list_sv_included_files(all_src_files:list, known_incdir_paths:list, target:str='',
                               warnings:bool=True,
                               modify_files_and_save_to_path=None,
                               unmodified_files_link_to_path=None) -> list:
    ''' Given a list of all_src_files, and list of known_incdir_paths, returns a list
    of all included files (fullpath). This is recurisve if an included file includes another file.

    Optional args -
    target -- (str) for debug purposes, the original DEPS target
    warnings -- (bool) False to disable warnings
    modify_files_and_save_to_path -- (str: directory/path) if you wish to strip all path information
      on the `include "(path)" for example:
        `include "foo.svh" -- no modifications
        `include "../bar.svh" -- is modified to become `include "bar.svh"
      Set to None (default) to disable.
    unmodified_files_link_to_path -- (str: directory/path) if you wish to symlink unmodified
      files to this path. Set to None (default) to disable.
    '''

    # order shouldn't matter, these will get added to the testrunner's filelist and
    # be included with +incdir+.

    sv_included_files_dict = dict() # key, value is if we've traversed it (bool)

    for fname in all_src_files:
        included_files_list = find_sv_included_files_within_file(
            filename=fname,
            known_incdir_paths=known_incdir_paths,
            warnings=warnings,
            modify_files_and_save_to_path=modify_files_and_save_to_path,
            unmodified_files_link_to_path=unmodified_files_link_to_path
        )

        for f in included_files_list:
            if f not in sv_included_files_dict:
                sv_included_files_dict[f] = False # add entry, mark it not traversed.

    for _ in range(_include_iteration_max_depth):
        # do these for a a depth of recurisve levels, in case `include'd file includes another file.
        # If we have more than N levels of `include hunting, then rethink this.
        # For example, some codebases would do their file dependencies as `include
        # as part of their header guards, which could be ~100 levels of nesting.
        for fname,traversed in sv_included_files_dict.items():
            if not traversed:
                included_files_list = find_sv_included_files_within_file(
                    filename=fname,
                    known_incdir_paths=known_incdir_paths,
                    warnings=warnings,
                    modify_files_and_save_to_path=modify_files_and_save_to_path,
                    unmodified_files_link_to_path=unmodified_files_link_to_path
                )
                sv_included_files_dict[fname] = True # mark as traversed.

                for f in included_files_list:
                    if f not in sv_included_files_dict:
                        sv_included_files_dict[f] = False # add entry, mark it not traversed.

    if not all(sv_included_files_dict.values()):
        # we had some that we're traversed.
        not_traversed = [k for k,v in sv_included_files_dict.items() if not v]
        error(f'Depth {_include_iteration_max_depth=} exceeded in looking for `includes,' \
              + f' {target=} {not_traversed=}')


    ret = list()
    for fname,traversed in sv_included_files_dict.items():
        if traversed:
            # add all the included files (should be traversed!) to our return list
            ret.append(fname)

    return ret


class ExportHelper:

    def __init__(self, cmd_design_obj, eda_command='export', out_dir=None, target=''):
        self.cmd_design_obj = cmd_design_obj
        self.eda_command = eda_command
        self.out_dir = out_dir
        self.target = target

        self.args = self.cmd_design_obj.args # lazy alias.
        self.included_files = list()
        self.out_deps_file = None

        # TODO(drew) It would be neat if I could export an "eda multi" command, like
        # CommandMulti that only gave me the list of all targets from a wildcard?
        # Because then I could create exports for each individual target, but lump
        # all files together and have a single exported DEPS.yml with unique targets.

    def do_it(self, check_if_overwrite:bool=False,
              deps_file_args:list=list(),
              test_json_eda_config:dict=dict(), **kwargs):

        self.make_out_dir(check_if_overwrite)
        self.write_files_to_out_dir()
        self.create_deps_yml_in_out_dir(deps_file_args=deps_file_args)

        if self.args.get('export-test-json', False):
            self.create_test_json_in_out_dir(eda_config=test_json_eda_config, **kwargs)

        info(f'export_helper: done - wrote to: {self.out_dir}')


    def make_out_dir(self, check_if_overwrite:bool=False):
        assert self.args.get('top', ''), f'Need "top" to be set'

        if not self.out_dir:
            if self.args.get('output', '') == "":
                self.out_dir = os.path.join('.', 'eda.export', self.args['top'] + '.export')

        if check_if_overwrite and self.args.get('force', False):
            if os.path.exists(self.out_dir):
                util.error(f"export_helper: output directory {out_dir} exists, use --force to overwrite")

        if not os.path.exists(self.out_dir):
            info(f"export_helper: Creating {self.out_dir} for exported file tree")
            util.safe_mkdir(self.out_dir)

    def write_files_to_out_dir(self):

        # Also sets our list of included files.
        self.included_files = get_list_sv_included_files(
            all_src_files=self.cmd_design_obj.files_sv + self.cmd_design_obj.files_v,
            known_incdir_paths=self.cmd_design_obj.incdirs,
            target=self.target,
            modify_files_and_save_to_path=self.out_dir,
            unmodified_files_link_to_path=self.out_dir
        )
        info(f"export_helper: {self.target=} included files {self.included_files=}")

    def create_deps_yml_in_out_dir(self, deps_file_args:list=list()):
        if not self.target:
            self.target = 'test'
        else:
            # Need to stip path information from self.target, b/c it will
            # be a Table key:
            self.target = os.path.split(self.target)[1]

        info(f'export_helper: Creating DEPS.yml for {self.target=} in {self.out_dir=}')

        # Need to strip path information from our files_sv and files_v:
        deps_files = list()
        for fullpath in self.cmd_design_obj.files_sv + self.cmd_design_obj.files_v:
            filename = os.path.split(fullpath)[1]
            deps_files.append(filename)


        data = {
            self.target: {
                'incdirs': '.',
                'deps': deps_files,
            }
        }

        if len(deps_file_args) > 0:
            data[self.target]['args'] = deps_file_args.copy()

        if self.args.get('top', None):
            data[self.target]['top'] = self.args['top']

        if len(self.cmd_design_obj.defines.keys()) > 0:
            data[self.target]['defines'] = self.cmd_design_obj.defines.copy()
            for define in _remove_DEPS_yml_defines:
                # Remove defines keys for OC_ROOT and OC_SEED. Change OC_SEED to _ORIG_OC_SEED
                if define in data[self.target]['defines']:
                    data[self.target]['defines'].pop(define)

        dst = os.path.join(self.out_dir, 'DEPS.yml')
        self.out_deps_file = dst
        util.yaml_safe_writer(data=data, filepath=dst)


    def create_test_json_in_out_dir(self, eda_config:dict=dict(), **kwargs):

        # We aren't going to do this if the eda_command was 'export':
        if not self.eda_command:
            return
        if self.eda_command == 'export':
            return

        # assumes we've run self.create_deps_yml_in_out_dir():
        assert self.target
        assert self.out_deps_file

        data = {
            'name': self.target,
            'eda': {
                'enable': True,
                'multi': False, # Not yet implemented.
                'command': self.eda_command,
                'targets': [self.target],
                'args': list(),
                'waves': self.args.get('waves', False),
                # tool - eda.CommandSimVerilator has this set in self.args:
                'tool': self.args.get('tool', None),
            },
            'files': list(),
        }

        # allow caller to override eda - tool, or eda - args, etc.
        for k,v in eda_config.items():
            if k in data['eda'].keys() and v is not None:
                data['eda'][k] = v

        # Note that args may already be set via:
        #   create_deps_yml_in_out_dir(deps_file_args=some_list)
        # For example, eda.CommandSim.do_export() will set certain allow-listed
        # args if present with non-default values.


        all_files = [self.out_deps_file] + self.included_files \
            + self.cmd_design_obj.files_sv + self.cmd_design_obj.files_v

        for somefile in all_files:
            assert os.path.exists(somefile)
            with open(somefile) as f:
                filestr = ''.join(f.readlines())
                data['files'].append({
                    'name': os.path.split(somefile)[1],
                    'content': filestr,
                })


        dst = os.path.join(self.out_dir, 'test.json')
        with open(dst, 'w') as f:
            json.dump(data, f)
            f.write('\n')
        info(f'export_helper: Wrote {dst=}')
