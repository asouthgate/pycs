from pycs.interfaces.CommandABC import CommandABC

class CommandExecutor:
    """ Class used to manage execution of commands. """

    def __init__(self):
        # Inverse command history to record operations needed to undo
        self.command_history = []
        # Every undo operation pops from command_history and adds to undo_history for redo
        self.undo_history = []

    def execute(self, command: CommandABC):
        """ Execute a command """
        command.execute()
        self.command_history.append(command)
    
    def undo(self):
        """ Undo a command """
        command = self.command_history.pop()
        command.undo()
        self.undo_history.append(command)

    def redo(self):
        """ Redo a command """
        command = self.undo_history.pop()
        command.execute()
        self.command_history.append(commmand)


