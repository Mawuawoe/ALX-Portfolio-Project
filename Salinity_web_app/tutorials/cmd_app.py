#!/usr/bin/python3
"""
a command line interpreter app demo1
"""
import cmd


class Mycmd(cmd.Cmd):
    # This the command prompt shown to the user
    prompt = 'mgcli>'
    intro = 'Welcome to my CLI! Type ? to list all commands'

    # commands are defined as methods starting with 'do_'
    def do_greet(self, line):
        """ a cmd to say hello"""
        print("Hello!")

    # the do exit is the cmd to close the app
    # and returning True exits the command loop
    def do_exit(self, line):
        """cmd to exit"""
        print("Goodbye")
        return True
    
    def do_add(self, line):
        numbers = map(int, line.split())
        print (f"Result is: {sum(numbers)}")
    
    #You can handle errors by defining a default method, 
    #which is called when the user types an unrecognized 
    # command:
    def default(self, line):
        print(f"Unknown command: {line} see help")

    # customize the help message for each command
    def help_greet(self):
        print("Greets the user")


# the command that starts the program
if __name__ == '__main__':
    Mycmd().cmdloop()
