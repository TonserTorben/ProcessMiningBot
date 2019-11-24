class ExecutionObject:
    def __init__(self, intent, command, command_help, function, execution, reply_type, ask_for_file, change_state):
        self.intent = intent                # navn på intent e.g. alpha
        self.command = command              # navn på kommando e.g. /alpha
        self.command_help = command_help    # Forklarende tekst om kommando
        self.function = function            # indeholder funktionen der skal kaldes e.g. pm.do_alpha !! MEN UDEN PARANTESER OG ARGUMENTER så er det en reference af funktionen og ikke en instans
        self.execution = execution          # navn på execution enum, til brug i execute_command funktion
        self.reply_type = reply_type        # navn på reply_type e.g. ReplyType.photo
        self.ask_for_file = ask_for_file    # en boolean om der skal spørges om der skal benyttes nuværende fil eller en anden
        self.change_state = change_state    # en boolean om bot state skal ændres til mining eller noget andet