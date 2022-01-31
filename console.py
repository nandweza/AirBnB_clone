#!/usr/bin/python3
"""contains the entry point of command interpreter"""
import cmd
import re
from models import storage


class HBNBCommand(cmd.Cmd):
    """command interpreter to interact with storage"""
    prompt = '(hbnb) '

    def parseline(self, line):
        """perform processing for command"""
        if '.' in line and '(' in line and ')' in line:
            toks = re.split(r'\.|\(|\)', line)
            toks[2] = toks[2].strip('"').replace(',', ' ')
            newline = toks[1] + ' ' + toks[0] + ' ' + toks[2]
            line = (toks[1], toks[0] + ' ' + toks[2], newline)
            if toks[1] == 'count':
                self.count(toks[0])
                return cmd.Cmd.parseline(self, '')
            return line
        return cmd.Cmd.parseline(self, line)

    def count(self, cls):
        """retrieves the number of instance of class"""
        n = 0
        for k, v in storage.all().items():
            if type(v).__name__ == cls:
                n += 1
        print(n)

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def do_create(self, arg):
        """Create new instance of class, saves it and prints the id"""
        args = arg.split()
        if self.validate_arg(args, False, False):
            obj = storage.classes()[args[0]]()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Show prints the string repr of an instance based on the class name
        and id"""
        args = arg.split()
        if self.validate_arg(args):
            key = args[0] + "." + args[1]
            print(storage.all()[key])

    def do_destroy(self, arg):
        """Destroy deletes an instance based on the class name and id"""
        args = arg.split()
        if self.validate_arg(args):
            key = args[0] + "." + args[1]
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """All prints all string repr of all instances based or not on the
        class name"""
        args = arg.split()
        if len(args) == 0:
            print([str(v) for k, v in storage.all().items()])
        else:
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                print([str(v) for k, v in storage.all().items()
                       if type(v).__name__ == args[0]])

    def do_update(self, arg):
        """Update updates an instance based on the class name and
        id by adding or updating attributes"""
        args = arg.split()
        if self.validate_arg(args):
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            key = args[0] + '.' + args[1]
            obj = storage.all()[key]
            if args[3].isdigit():
                args[3] = float(args[3])
                args[3] = int(args[3]) if args[3].is_integer() else args[3]
            else:
                if args[3].startswith('"'):
                    args[3] = arg.partition('"')[2].rpartition('"')[0]
            setattr(obj, str(args[2]), args[3])
            storage.save()

    def validate_arg(self, args, validate_id=True, check_existence=True):
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
            return False
        if len(args) < 2 and validate_id:
            print("** instance id missing **")
            return False
        if check_existence and args[0] + "." + args[1] not in storage.all():
            print("** no instance found **")
            return False
        return True

    def emptyline(self) -> bool:
        """called when an empty line is entered"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
