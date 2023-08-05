# -*- coding: utf-8 -*-

"""

Centralized use of plumbum package:
http://plumbum.readthedocs.org/en/latest/index.html#

- use shell commands in a more pythonic way -

TODO: also consider switching to this other one https://amoffat.github.io/sh/

"""

from utilities.logs import get_logger
log = get_logger(__name__)

try:
    from plumbum.commands.processes import ProcessExecutionError
except ImportError as e:
    log.critical_exit("\nThis module requires an extra package:\n%s" % e)


class BashCommands(object):
    """ Wrapper for execution of commands in a bash shell """

    _shell = None

    def __init__(self):
        """
        Load my personal list of commands based on my bash environment
        """
        from plumbum import local as myshell
        self._shell = myshell

        super(BashCommands, self).__init__()
        log.very_verbose("Internal shell initialized")

    def execute_command(
            self, command, parameters=None, env=None,
            customException=None):
        try:

            if parameters is None:
                parameters=[]

            # Pattern in plumbum library for executing a shell command
            command = self._shell[command]
            # Specify different environment variables
            if env is not None:
                command = command.with_env(**env)
            log.verbose("Executing command %s %s" % (command, parameters))
            return command(parameters)

        except ProcessExecutionError as e:
            if customException is None:
                raise(e)
            else:
                # argv = e.argv
                # retcode = e.retcode
                # stdout = e.stdout
                stderr = e.stderr

                raise customException(stderr)

    def execute_command_advanced(
            self, command, parameters=None, customException=None,
            retcodes=()):  # pylint:disable=too-many-arguments
        try:
            if parameters is None:
                parameters=[]

            # Pattern in plumbum library for executing a shell command
            # e.g. ICOM["list"][irods_dir].run(retcode = (0,4))
            # FIXME: does not work if parameters is bigger than one element
            comout = \
                self._shell[command][parameters].run(retcode=retcodes)
            log.verbose("Executed command %s %s" % (command, parameters))
            # # NOTE: comout is equal to (status, stdin, stdout)
            return comout

        except ProcessExecutionError as e:
            if customException is None:
                raise(e)
            else:
                # argv = e.argv
                # retcode = e.retcode
                # stdout = e.stdout
                stderr = e.stderr

                raise customException(stderr)

    ###################
    # BASE COMMANDS
    def create_empty(self, path, directory=False, ignore_existing=False):

        args = []
        if not directory:
            com = "touch"
        else:
            com = "mkdir"
            if ignore_existing:
                args.append("-p")
        args.append(path)
        # Debug
        self.execute_command(com, args)
        log.debug("Created %s", path)

    def remove(self, path, recursive=False, force=False):

        # Build parameters and arguments for this command
        com = "rm"
        args = []
        if force:
            args.append('-f')
        if recursive:
            args.append('-r')
        args.append(path)
        # Execute
        self.execute_command(com, args)
        # Debug
        log.debug("Removed %s", path)

    ###################
    # DIRECTORIES
    def create_directory(self, directory, ignore_existing=True):
        self.create_empty(directory,
                          directory=True, ignore_existing=ignore_existing)

    def remove_directory(self, directory, ignore=False):
        self.remove(directory, recursive=True, force=ignore)

    def replace_in_file(self, target, destination, file):
        params = [
            "-i", "--",
            "s/%s/%s/g" % (target, destination),
            file
        ]
        self.execute_command("sed", params)

    def copy(self, target, destination):

        params = [target, destination]
        self.execute_command("cp", params)

    def copy_folder(self, target, destination):

        params = ["-r", target, destination]
        self.execute_command("cp", params)
