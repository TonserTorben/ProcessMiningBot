class ExecutionObject:
    def __init__(self, intent, function, reply_type, command = None, command_help = None, execution=None, 
                    new_state = None, ask_for_file = False, change_state = False, script_from_db = False, script_name = None):
        self.intent = intent                    # name of intent e.g. alpha
        self.command = command                  # name of command e.g. /alpha
        self.command_help = command_help        # Text explaining the command, used in the help text
        self.function = function                # Contains the function which should be executed by this intent e.g. pm.do_alpha (BUT ONLY A REFERENCE TO THE FUNCTION!) hence the missing parenthases and arguments
        self.execution = execution              # Type of execution enum, Used for knowing what kind of input the objects function will be expecting
        self.reply_type = reply_type            # Type of reply e.g. ReplyType.photo
        self.ask_for_file = ask_for_file        # A boolean that tells whether or not the user should be prompted which file should be used
        self.change_state = change_state        # A boolean that tells whether or not the state of the bot is changing by this intent
        self.new_state = new_state              # The new state of the bot
        self.script_from_db = script_from_db    # Boolean that tells whether or not the function should fetch script from database
        self.script_name = script_name          # Name of the script in case such exists.