from ..base import OptionsGroup, ParametrizedValue
from ..utils import listify


class HookAction(ParametrizedValue):

    pass


class ActionMount(HookAction):
    """Mount or unmount filesystems.

    Examples:
        * Mount: proc none /proc
        * Unmount: /proc

    """

    name = 'mount'

    def __init__(self, mountpoint, fs=None, src=None, flags=None):
        """

        :param str|unicode mountpoint:

        :param str|unicode fs: Filesystem. Presence indicates mounting.

        :param str|unicode src: Presence indicates mounting.

        :param str|unicode|list flags: Flags available for the operating system.
            As an example on Linux you will options like: bind, recursive, readonly, rec, detach etc.

        """
        if flags is not None:
            flags = listify(flags)
            flags = ','.join(flags)

        if fs:
            args = [fs, src, mountpoint, flags]

        else:
            args = [mountpoint, flags]
            self.name = 'umount'

        super(ActionMount, self).__init__(*args)


class ActionExecute(HookAction):
    """Run the shell command.

    Command run under ``/bin/sh``.
    If for some reason you do not want to use ``/bin/sh``,
    use ``binsh`` option,

    Examples:
        * cat /proc/self/mounts

    """

    name = 'exec'

    # todo consider adding safeexec
    def __init__(self, command):
        super(ActionExecute, self).__init__(command)


class ActionCall(HookAction):
    """Call functions in the current process address space."""

    name = 'call'

    def __init__(self, target, honour_exit_status=False, arg_int=False):
        """
        :param str|unicode target: Symbol and args.

        :param bool honour_exit_status: Expect an int return.
            Anything != 0 means failure.

        :param bool arg_int: Parse the argument as an int.

        """
        name = self.name

        if arg_int:
            name += 'int'

        if honour_exit_status:
            name += 'ret'

        self.name = name

        super(ActionCall, self).__init__(target)


class ActionDirChange(HookAction):
    """Changes a directory.

    Convenience action, same as ``call:chdir <directory>``.

    """
    name = 'cd'

    def __init__(self, target_dir):
        super(ActionDirChange, self).__init__(target_dir)


class ActionDirCreate(HookAction):
    """Creates a directory with 0777."""

    name = 'mkdir'

    def __init__(self, target_dir):
        super(ActionDirCreate, self).__init__(target_dir)


class ActionFileCreate(HookAction):
    """Creates a directory with 0666."""

    name = 'create'

    def __init__(self, fpath):
        super(ActionFileCreate, self).__init__(fpath)


class ActionExit(HookAction):
    """Exits.

    Convenience action, same as ``callint:exit [num]``.

    """
    name = 'exit'

    def __init__(self, status_code=None):
        super(ActionExit, self).__init__(status_code)


class ActionPrintout(HookAction):
    """Prints.

    Convenience action, same as calling the ``uwsgi_log`` symbol.

    """
    name = 'print'

    def __init__(self, text=None):
        super(ActionPrintout, self).__init__(text)


class ActionSetHostName(HookAction):
    """Sets a host name."""

    name = 'hostname'

    def __init__(self, name):
        super(ActionSetHostName, self).__init__(name)


class ActionAlarm(HookAction):
    """Issues an alarm. See ``.alarms`` options group."""

    name = 'alarm'

    def __init__(self, alarm, message):
        super(ActionAlarm, self).__init__(alarm, message)


class ActionFileWrite(HookAction):
    """Writes a string to the specified file.

    If file doesn't exist it will be created.

    .. note:: Since 1.9.21

    """
    name = 'write'

    def __init__(self, target, text, append=False, newline=False):
        """

        :param str|unicode target: File to write to.

        :param str|unicode text: Text to write into file.

        :param bool append: Append text instead of rewrite.

        :param bool newline: Add a newline at the end.

        """
        if append:
            self.name = 'append'

        if newline:
            self.name += 'n'

        super(ActionFileWrite, self).__init__(target, text)


class ActionFifoWrite(HookAction):
    """Writes a string to the specified FIFO (see ``fifo_file`` from ``master_process`` params)."""

    name = 'writefifo'

    def __init__(self, target, text, wait=False):
        """
        :param bool wait: Wait until FIFO is available.

        """
        if wait:
            self.name = 'spinningfifo'

        super(ActionFifoWrite, self).__init__(target, text)


class ActionUnlink(HookAction):
    """Unlink the specified file.

    .. note:: Since 1.9.21

    """
    name = 'unlink'

    def __init__(self, target):
        super(ActionUnlink, self).__init__(target)


class MainProcess(OptionsGroup):
    """Main process is the uWSGI process.

    .. warning:: Do not run uWSGI instances as root.
        You can start your uWSGIs as root, but be sure to drop privileges
        with the ``uid`` and ``gid`` options from ``set_owner_params``.

    """

    class actions(object):
        """Actions available for ``.set_hook()``."""

        alarm = ActionAlarm
        call = ActionCall
        dir_change = ActionDirChange
        dir_create = ActionDirCreate
        execute = ActionExecute
        exit = ActionExit
        fifo_write = ActionFifoWrite
        file_create = ActionFileCreate
        file_write = ActionFileWrite
        mount = ActionMount
        printout = ActionPrintout
        set_host_name = ActionSetHostName
        unlink = ActionUnlink

        # todo consider adding:
        # putenv, chmod/sticky, chown/chown2, rpc/retryrpc, unix_signal
        # wait_for_fs/wait_for_file/wait_for_dir, wait_for_socket

    class phases:
        """Phases available for hooking using ``.set_hook()``.

        Some of them may be **fatal** - a failing hook for them
        will mean failing of the whole uWSGI instance (generally calling exit(1)).

        """

        ASAP = 'asap'
        """As soon as possible. **Fatal**
        
        Run directly after configuration file has been parsed, before anything else is done.
        
        """

        JAIL_PRE = 'pre-jail'
        """Before jailing. **Fatal** 
        
        Run before any attempt to drop privileges or put the process in some form of jail.        
        
        """

        JAIL_IN = 'in-jail'
        """In jail after initialization. **Fatal** 

        Run soon after jayling, but after post-jail. 
        If jailing requires fork(), the chidlren run this phase.
        
        """

        JAIL_POST = 'post-jail'
        """After jailing. **Fatal**
        
        Run soon after any jailing, but before privileges drop. 
        If jailing requires fork(), the parent process run this phase.
        
        """

        PRIV_DROP_PRE = 'as-root'
        """Before privileges drop. **Fatal**
        
        Last chance to run something as root.
        
        """

        PRIV_DROP_POST = 'as-user'
        """After privileges drop. **Fatal**"""

        MASTER_START = 'master-start'
        """When Master starts."""

        EMPEROR_START = 'emperor-start'
        """When Emperor starts."""

        EMPEROR_STOP = 'emperor-stop'
        """When Emperor sent a stop message."""

        EMPEROR_RELOAD = 'emperor-reload'
        """When Emperor sent a reload message."""

        EMPEROR_LOST = 'emperor-lost'
        """When Emperor connection is lost."""

        EXIT = 'as-user-atexit'
        """Before app exit and reload."""

        APP_LOAD_PRE = 'pre-app'
        """Before app loading. **Fatal**"""

        APP_LOAD_POST = 'post-app'
        """After app loading. **Fatal**"""

        VASSAL_ON_DEMAND_IN = 'as-on-demand-vassal'
        """Whenever a vassal enters on-demand mode."""

        VASSAL_CONFIG_CHANGE_POST = 'as-on-config-vassal'
        """Whenever the emperor detects a config change for an on-demand vassal."""

        VASSAL_START_PRE = 'as-emperor-before-vassal'
        """Before the new vassal is spawned."""

        VASSAL_PRIV_DRP_PRE = 'as-vassal-before-drop'
        """In vassal, before dropping its privileges."""

        VASSAL_SET_NAMESPACE = 'as-emperor-setns'
        """In the emperor entering vassal namespace."""

        VASSAL_START_IN = 'as-vassal'
        """In the vassal before executing the uwsgi binary. **Fatal** 
        
        In vassal on start just before calling exec() directly in the new namespace.
        
        """

        VASSAL_START_POST = 'as-emperor'
        """In the emperor soon after a vassal has been spawn.
         
        Setting 4 env vars:
            * UWSGI_VASSAL_CONFIG 
            * UWSGI_VASSAL_PID
            * UWSGI_VASSAL_UID 
            * UWSGI_VASSAL_GID

        """

        GATEWAY_START_IN_EACH = 'as-gateway'
        """In each gateway on start."""

        MULE_START_IN_EACH = 'as-mule'
        """In each mule on start."""

        WORKER_ACCEPTING_PRE_EACH = 'accepting'
        """Before the each worker starts accepting requests. 
        
        .. note:: Since 1.9.21
        
        """

        WORKER_ACCEPTING_PRE_FIRST = 'accepting1'
        """Before the first worker starts accepting requests.
        
        .. note:: Since 1.9.21
        
        """

        WORKER_ACCEPTING_PRE_EACH_ONCE = 'accepting-once'
        """Before the each worker starts accepting requests, one time per instance. 
        
        .. note:: Since 1.9.21
        
        """

        WORKER_ACCEPTING_PRE_FIRST_ONCE = 'accepting1-once'
        """Before the first worker starts accepting requests, one time per instance.
        
        .. note:: Since 1.9.21
        
        """

    def set_basic_params(
            self, touch_reload=None, priority=None, vacuum=None, binary_path=None, honour_stdin=None):
        """

        :param str|list touch_reload: Reload uWSGI if the specified file or directory is modified/touched.

        :param int priority: Set processes/threads priority (``nice``) value.

        :param bool vacuum: Try to remove all of the generated files/sockets
            (UNIX sockets and pidfiles) upon exit.

        :param str|unicode binary_path: Force uWSGI binary path.
            If you do not have uWSGI in the system path you can force its path with this option
            to permit the reloading system and the Emperor to easily find the binary to execute.

        :param bool honour_stdin: Do not remap stdin to ``/dev/null``.
            By default, ``stdin`` is remapped to ``/dev/null`` on uWSGI startup.
            If you need a valid stdin (for debugging, piping and so on) use this option.

        """
        self._set('touch-reload', touch_reload, multi=True)
        self._set('prio', priority)

        self._set('vacuum', vacuum, cast=bool)
        self._set('binary-path', binary_path)
        self._set('honour-stdin', honour_stdin, cast=bool)

        return self._section

    def daemonize(self, log_into, after_app_loading=False):
        """Daemonize uWSGI.

        :param str|unicode log_into: Logging destination:

            * File: /tmp/mylog.log

            * UPD: 192.168.1.2:1717

                .. note:: This will require an UDP server to manage log messages.
                    Use ``networking.register_socket('192.168.1.2:1717, type=networking.SOCK_UDP)``
                    to start uWSGI UDP server.

        :param str|unicode bool after_app_loading: Whether to daemonize after
            or before applications loading.

        """
        self._set('daemonize2' if after_app_loading else 'daemonize', log_into)

        return self._section

    def set_owner_params(self, uid=None, gid=None, add_gids=None, set_asap=False):
        """Set process owner params - user, group.

        :param str|unicode|int uid: Set uid to the specified username or uid.

        :param str|unicode|int gid: Set gid to the specified groupname or gid.

        :param list|str|unicode|int add_gids: Add the specified group id to the process credentials.
            This options allows you to add additional group ids to the current process.
            You can specify it multiple times.

        :param bool set_asap: Set as soon as possible.
            Setting them on top of your vassal file will force the instance to setuid()/setgid()
            as soon as possible and without the (theoretical) possibility to override them.

        """
        prefix = 'immediate-' if set_asap else ''

        self._set(prefix + 'uid', uid)
        self._set(prefix + 'gid', gid)
        self._set('add-gid', add_gids, multi=True)

        return self._section

    def set_hook(self, phase, action):
        """Allows setting hooks (attaching actions) for various uWSGI phases.

        :param str|unicode phase: See constants in ``.phases``.

        :param str|unicode|list|HookAction|list[HookAction] action:

        """
        self._set('hook-%s' % phase, action, multi=True)

        return self._section

    def set_hook_touch(self, fpath, action):
        """Allows running certain action when the specified file is touched.

        :param str|unicode fpath: File path.

        :param str|unicode|list|HookAction|list[HookAction] action:

        """
        self._set('hook-touch', '%s %s' % (fpath, action), multi=True)

        return self._section

    def set_hook_after_request(self, func):
        """Run the specified function/symbol (C level) after each request.

        :param str|unicode func:

        """
        self._set('after-request-hook', func, multi=True)

        return self._section

    def set_on_exit_params(self, skip_hooks=None, skip_teardown=None):
        """Set params related to process exit procedure.

        :param bool skip_hooks: Skip ``EXIT`` phase hook.

            .. note:: Ignored by the master.

        :param bool skip_teardown: Allows skipping teardown (finalization) processes for some plugins.

            .. note:: Ignored by the master.

            Supported by:
                * Perl
                * Python

        """
        self._set('skip-atexit', skip_hooks, cast=bool)
        self._set('skip-atexit-teardown', skip_teardown, cast=bool)

        return self._section

    def run_command_on_event(self, command, phase=phases.ASAP):
        """Run the given command on a given phase.

        :param str|unicode command:

        :param str|unicode phase: See constants in ``Phases`` class.

        """
        self._set('exec-%s' % phase, command, multi=True)

        return self._section

    def run_command_on_touch(self, command, target):
        """Run command when the specified file is modified/touched.

        :param str|unicode command:

        :param str|unicode target: File path.

        """
        self._set('touch-exec', '%s %s' % (target, command), multi=True)

        return self._section

    def set_pid_file(self, fpath, before_priv_drop=True, safe=False):
        """Creates pidfile before or after privileges drop.

        :param str|unicode fpath: File path.

        :param bool before_priv_drop:

        :param bool safe: The safe-pidfile works similar to pidfile
            but performs the write a little later in the loading process.
            This avoids overwriting the value when app loading fails,
            with the consequent loss of a valid PID number.

        """
        command = 'pidfile'

        if not before_priv_drop:
            command += '2'

        if safe:
            command = 'safe-' + command

        self._set(command, fpath)

        return self._section

    def set_naming_params(self, autonaming=None, prefix=None, suffix=None, name=None):
        """Setups processes naming parameters.

        :param bool autonaming: Automatically set process name to something meaningful.
            Generated process names may be 'uWSGI Master', 'uWSGI Worker #', etc.

        :param str prefix: Add prefix to process names.

        :param str suffix: Append string to process names.

        :param str name: Set process names to given static value.

        """
        self._set('auto-procname', autonaming, cast=bool)
        self._set('procname-prefix%s' % ('-spaced' if prefix and prefix.endswith(' ') else ''), prefix)
        self._set('procname-append', suffix)
        self._set('procname', name)

        return self._section
