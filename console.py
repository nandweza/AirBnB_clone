#!/usr/bin/python3
"""contains the entry point of command interpreter"""
import cmd


class HBNBCommand(cmd.Cmd):
    """command interpreter to interact with storage"""
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self) -> bool:
        """called when an empty line is entered"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
