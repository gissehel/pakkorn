class Command(object) :
    """This class store every aspects of a 'Command', which can be a command line or a name used internally by windows to uninstall a program."""

    def __init__(self,line=None,uninstall_winname=None,command=None) :
        if line is None and uninstall_winname is None and command is None :
            raise ValueError("either 'line', 'uninstall_winname' or 'command' should be different from None")
        if (line is not None and uninstall_winname is not None) and command is None :
            raise ValueError("'line' and 'uninstall_winname' can't both be different from None")
        if command is None :
            self._line = line
            self._uninstall_winname = uninstall_winname
        else : 
            self._line = command._line
            self._uninstall_winname = command._uninstall_winname

    def __str__(self) :
        if self._line is not None :
            return self._line
        return '!' + self._uninstall_winname

    def is_uninstall_winname(self) :
        return self._uninstall_winname is not None

    def get_uninstall_winname(self) :
        return self._uninstall_winname

class Commands(object) :
    """This class store every aspects of a 'Commands', with is a set of 'Command' to install, uninstall, etc."""
    
    def __init__(self,commands=None) :
        self._commands = []
        if commands is not None :
            for command in commands :
                self._commands.append(Command(command=command))

    def add_command(self,line=None,uninstall_winname=None) :
        self._commands.append(Command(line,uninstall_winname))

    def __delitem__(self,index) :
        del self._commands[index]

    def __getitem__(self,index) :
        return self._commands[index]

    def __setitem__(self,index,command) :
        self._commands[index] = command

    def __iter__(self) :
        return iter(self._commands)
