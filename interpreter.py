import re

class Interpreter(object):
    """
    The interpreter turns matches commands with functions. It strongly relies
    on the Command object, bundling them together into a bigger regex.
    """

    # The name with which all commands begin. Can be a word or a regex.
    # Example: jenkins, alfred, robot. "Jenkins! Turn on the lights!"
    signal = "jenkins"

    # Command prefixes and suffixes. Can be a tuple of words or a regex
    prefixes = "( can you| could you)?( please)?"
    suffixes = "( please)?"

    # The actual commands. Expects a list of Command objects
    commands = ()

    def __init__(self, commands):
        """
        Prepares the interpreter, compile the regex strings
        """
        self.commands = commands
        self.regex = self.regex()

    def regex(self):
        """
        Build a regex to match all possible commands
        """
        # Basic command structure
        basic_command = "{signal}{prefix} {command}{suffix}"

        # Build the command regex by joining individual regexes
        # e.g. (command_1|command_2|command_3)
        command_regexes = []
        for command in self.commands:
            command_regexes.append(command.regex)
        command_regex = "({0})".format("|".join(command_regexes))

        # Wrap the command with the prefix and suffix regexes
        final_regex = basic_command.format(
            signal = self.signal,
            command = command_regex,
            prefix = self.prefixes,
            suffix = self.suffixes,
        )

        # Return the compiled regex, ready to be used
        return re.compile(final_regex)

    def match(self, command):
        # Try matching the command to an action
        result = self.regex.match(command)
        if result:
            groups = result.groupdict()  # Get all the group matches from the regex

            print("Got '%s'" % command)

            for command in self.commands:
                # Check if the command name matches a regex group
                if command.name in groups and groups[command.name] is not None:
                    subject = None
                    if command.subjects:
                        subject = groups[command.name + 'Subject']  # The group of the subject ('the lights' in 'turn on the lights')
                    command.dispatch(subject)
            print("???")
        else:
            print("Could not match '{0}' to a command using regex".format(command))