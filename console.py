#!/usr/bin/python3
"""Defining the project console
It will be the entry point of the command interpreter"""
import cmd
from shlex import split
import re
from models import storage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
from models import classes


def arg_parse(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    brkt = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brkt is None:
            return[j.strip(",") for j in split(arg)]
        else:
            lx = split(arg[:brkt.span()[0]])
            rtl = [j.strip(",") for j in lx]
            rtl.append(brkt.group())
            return rtl
    else:
        lx = split(arg[:braces.span()[0]])
        rtl = [j.strip(",") for j in lx]
        rtl.append(braces.group())
        return rtl


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter.
    Atrr:
       prompt: command prompt. Should be a string
    """
    all_classes = classes
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Empty line should not execute anything"""
        pass

    def default(self, arg):
        """Default behaviour when input is invalid"""
        dict_argument = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        test = re.search(r"\.", arg)
        if test is not None:
            larg = [arg[:test.span()[0]], arg[test.span()[1]:]]
            test = re.search(r"\((.*?)\)", larg[1])
            if test is not None:
                command = [larg[1][:test.span()[0]], test.group()[1:-1]]
                if command[0] in dict_argument.keys():
                    call = "{} {}".format(larg[0], command[1])
                    return dict_argument[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """End of File signal to exit the program"""
        print("")
        return True

    def do_create(self, arg):
        """Creating a new instance of class and printing id"""
        larg = split(arg)
        if len(larg) == 0:
            print("** class name missing **")
        elif larg[0] not in self.all_classes:
            print("** class doesn't exist **")
        else:
            cls = self.all_classes[larg[0]]
            obj = cls()
            if len(larg) > 1:
                for i in range(1, len(larg)):
                    pair = larg[i].split('=')
                    if len(pair) == 2:
                        pair[1] = pair[1].replace('_', ' ')
                        try:
                            setattr(obj, pair[0], eval(pair[1]))
                        except (SyntaxError, NameError):
                            setattr(obj, pair[0], pair[1])
                storage.new(obj)
            print(obj.id)
            obj.save()

    def do_show(self, arg):
        """Show the string representation of a class of given id"""
        larg = arg_parse(arg)
        dict_object = storage.all()
        if len(larg) == 0:
            print("** class name missing **")
        elif larg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(larg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(larg[0], larg[1]) not in dict_object:
            print("** no instance found **")
        else:
            print(dict_object["{}.{}".format(larg[0], larg[1])])

    def do_destroy(self, arg):
        """Delete a class of a particular id"""
        larg = arg_parse(arg)
        dict_object = storage.all()
        if len(larg) == 0:
            print("** class name missing **")
        elif larg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(larg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(larg[0], larg[1]) not in dict_object.keys():
            print("** no instance found **")
        else:
            del dict_object["{}.{}".format(larg[0], larg[1])]
            storage.save()

    def do_all(self, arg):
        """Print all string representation of all instances
        based or not on the class name"""
        larg = arg_parse(arg)
        if len(larg) > 0 and larg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objects = []
            for item in storage.all().values():
                if len(larg) > 0 and larg[0] == item.__class__.__name__:
                    objects.append(item.__str__())
                elif len(larg) == 0:
                    objects.append(item.__str__())
            print(objects)

    def do_count(self, arg):
        """Get the number of instances of a given class"""
        larg = arg_parse(arg)
        counter = 0
        for item in storage.all().values():
            if larg[0] == item.__class__.__name__:
                counter += 1
        print(counter)

    def do_update(self, arg):
        """Update an instance based on the class name and
        id by adding or updating attribute"""
        larg = arg_parse(arg)
        dict_object = storage.all()

        if len(larg) == 0:
            print("** class name missing **")
            return False
        if larg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(larg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(larg[0], larg[1]) not in dict_object.keys():
            print("** no instance found **")
            return False
        if len(larg) == 2:
            print("** attribute name missing **")
            return False
        if len(larg) == 3:
            try:
                type(eval(larg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(larg) == 4:
            objct = dict_object["{}.{}".format(larg[0], larg[1])]
            if larg[2] in objct.__class__.__dict__.keys():
                type_val = type(objct.__class__.__dict__[larg[2]])
                objct.__dict__[larg[2]] = type_val(larg[3])
            else:
                objct.__dict__[larg[2]] = larg[3]
        elif type(eval(larg[2])) == dict:
            objct = dict_object["{}.{}".format(larg[0], larg[1])]
            for a, b in eval(larg[2]).items():
                if (a in objct.__class__.__dict__.keys() and
                        type(objct.__class__.__dict__[a])
                        in {str, int, float}):
                    type_val = type(objct.__class__.__dict__[a])
                    objct.__dict__[a] = type_val(b)
                else:
                    objct.__dict__[a] = b
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
