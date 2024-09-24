#!/usr/bin/python3
"""
A command-line interpreter app demo.
"""
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.salinity import Salinity
from models.pan import Pan
import shlex


classes = {"BaseModel": BaseModel,
           "User": User,
           "Salinity": Salinity,
           "Pan": Pan,
           }

class MyCmd(cmd.Cmd):
    """Command-line interpreter for managing BaseModel instances."""
    
    # Command prompt shown to the user
    prompt = 'mycli> '
    intro = 'Welcome to my CLI! Type ? or help to list all commands.'

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, line):
        """
        Create a new instance of BaseModel and save it.
        Usage: create BaseModel
        """
        cmd_args = line.split()
        
        if len(cmd_args) == 0:
            print("** class name missing **")
        elif cmd_args[0] not in classes:
            print("** class doesn't exist **")
        else:
            if len(cmd_args) < 2:
                instance = classes[cmd_args[0]]()
            else:
                new_dict = self._key_value_parser(cmd_args[1:])
                instance = classes[cmd_args[0]](**new_dict)
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """
        Show an instance of BaseModel based on class name and ID.
        Usage: show BaseModel <id>
        """
        cmd_args = shlex.split(line)

        if len(cmd_args) == 0:
            print("** class name missing **")
            return

        if cmd_args[0] not in classes:
            print("** class doesn't exist **")
            return

        if len(cmd_args) < 2:
            print("** instance id missing **")
            return

        key = f"{cmd_args[0]}.{cmd_args[1]}"
        all_objects = models.storage.all()

        if key not in all_objects:
            print("** no instance found **")
        else:
            obj = all_objects[key]
            print(obj)

    def do_destroy(self, line):
        """
        Delete an instance of BaseModel based on class name and ID.
        Usage: destroy BaseModel <id>
        """
        cmd_args = shlex.split(line)

        if len(cmd_args) == 0:
            print("** class name missing **")
            return

        if cmd_args[0] not in classes:
            print("** class doesn't exist **")
            return

        if len(cmd_args) < 2:
            print("** instance id missing **")
            return

        # Construct the key for the object (e.g., BaseModel.<id>)
        key = f"{cmd_args[0]}.{cmd_args[1]}"
        all_objects = models.storage.all()

        if key not in all_objects:
            print("** no instance found **")
        else:
            # Delete the object from the storage dictionary
            del all_objects[key]
            
            # Save the changes to the file storage
            models.storage.save()
            
            # Provide feedback to the user
            print(f"Instance with id {cmd_args[1]} was successfully deleted")

    def do_all(self, line):
        """
        Prints all string representations of instances, based or not on the class name.
        Usage: all [ClassName] or all
        The output will be a list of strings.
        """
        cmd_args = shlex.split(line)
        all_objects = models.storage.all()
        obj_list = []

        # If no class is specified, print all objects
        if len(cmd_args) == 0:
            for obj in all_objects.values():
                obj_list.append(str(obj))
            print(obj_list)
            return

        # Validate the class name
        if cmd_args[0] not in classes:
            print("** class doesn't exist **")
            return

        # Filter and print instances of the given class
        for obj in all_objects.values():
            if obj.__class__.__name__ == cmd_args[0]:
                obj_list.append(str(obj))

        print(obj_list)

    def do_update(self, arg):
        """
         Updates an instance based on the class name and id
         by adding or updating attribute
         (save the change into the JSON file).
         Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".
        """
        command = shlex.split(arg)

        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in classes:
            print("** class doesn't exist **")
        elif len(command) < 2:
            print("** instance id missing **")
        else:
            objects = models.storage.all()
            key = "{}.{}".format(command[0], command[1])
            if key not in objects:
                print("** no instance found **")
            elif len(command) < 3:
                print("** attribute name missing **")
            elif len(command) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                attr_name = command[2]
                attr_value = command[3]

                try:
                    attr_value = eval(attr_value)
                except Exception:
                    pass

                setattr(obj, attr_name, attr_value)
                obj.save()



    def do_quit(self, line):
        """
        Command to exit the program.
        Usage: quit
        """
        print("Goodbye")
        return True
    
    def do_EOF(self, arg):
        """
        EOF to quit the program
        """
        return True

    def emptyline(self):
        """
        Override the default behavior to do nothing on an empty input line.
        """
        pass

    def default(self, line):
        """
        Handle unrecognized commands.
        """
        print(f"Unknown command: {line}. Type ? or help for available commands.")


# Start the command-line interpreter
if __name__ == '__main__':
    MyCmd().cmdloop()
