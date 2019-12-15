from NLP.ExecutionObject import ExecutionObject as e_object
import PM.pm as pm
from Enums.reply_enum import ReplyType
from Enums.execution_enum import ExecutionState as Execution
from Enums.bot_state_enum import BotState
import NLP.HelperFunctions as execution
import Globals

context_manager = Globals.get_context_manager()

objects =  [e_object(intent="Alpha",
                     command="/alpha",
                     command_help="Does the alpha miner on the current log.", 
                     function=pm.do_alpha_miner, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),

            e_object(intent="Conformance", 
                     function="Okay, what kind of conformance check do you have in mind? \n Currently supported checks are: Fitness, Precision and a Complete conformance check covering both fitness, precision and simplicity checks",
                     reply_type=ReplyType.text, 
                     ask_for_file=True), #TO BE IMPLEMENTED

            e_object(intent="Conformance_complete_follow",
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file=True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Conformance_fitness_follow",
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file= True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Conformance_precision_follow",
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file= True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Conformance_complete",
                     command="/conformance_complete", 
                     command_help="Does complete conformance checking on the current log and model", 
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file= True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Conformance_fitness",
                     command="/conformance_fitness", 
                     command_help="Does fitness conformance checking on the current log and model", 
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file= True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Conformance_precision",
                     command="/conformance_precision",
                     command_help="Does precision conformance checking on the current log and model", 
                     function=pm.do_conformance, 
                     execution=Execution.Both, 
                     reply_type=ReplyType.text, 
                     ask_for_file= True, 
                     change_state=True,
                     new_state=BotState.Waiting_for_conformance_input),

            e_object(intent="Current_log",
                     command="/currentlog",
                     command_help="Shows the current log in this chat",
                     function=context_manager.get_current_log_name,
                     execution=Execution.Chat_id,
                     reply_type=ReplyType.text),

            e_object(intent="Current_log_name",
                     command="/currentlogname",
                     command_help="Shows the name of the current log in this chat",
                     function=context_manager.get_current_log_name,
                     execution=Execution.Chat_id,
                     reply_type=ReplyType.text),

            e_object(intent="Current_model",
                     command="/currentmodel",
                     command_help="Shows the current model in this chat",
                     function=pm.show_model,
                     execution=Execution.Chat_id,
                     reply_type=ReplyType.photo),

            e_object(intent="Current_model_name",
                     command="/currentmodelname",
                     command_help="Shows the name of the current model in this chat",
                     function=context_manager.get_current_model_name,
                     execution=Execution.Chat_id,
                     reply_type=ReplyType.text),

            e_object(intent="DescribeLog",
                     command="/describelog", 
                     command_help="Describes the current log", 
                     function=execution.get_log_description, 
                     execution=Execution.Chat_id, 
                     reply_type=ReplyType.multi, 
                     ask_for_file= True),

            e_object(intent="DFG",
                     function="What kind of directly follows graph would you like me to do? Resource or performance?",
                     reply_type=ReplyType.text, 
                     ask_for_file= True),

            e_object(intent="DFG_resource_follow",
                     function=pm.do_dfg_resource, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),

            e_object(intent="DFG_performance_follow",
                     function=pm.do_dfg_performance,
                     execution=Execution.Log,
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),

            e_object(intent="DFG_performance",
                     command="/dfg_performance", 
                     command_help="Makes a directly follows graph for performance", 
                     function=pm.do_dfg_performance, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),

            e_object(intent="DFG_resource",
                     command="/dfg_resource", 
                     command_help="Makes a directly follows graphs for resouces", 
                     function=pm.do_dfg_resource, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),  

            e_object(intent="Discovery",                     
                     function="Okay, what kind of discovery would you like to perform? \n Currently I support: dfg, alpha miner, inductive miner, description of the log, dotted charts and precedence matrix",  
                     reply_type=ReplyType.text),

            e_object(intent="Dottedchart",
                     function="What kind of dotted chart would you like me to do? Relative or absolute?",
                     reply_type=ReplyType.text, 
                     ask_for_file= True),

            e_object(intent="Dottedchart_absolute_follow",
                     function=pm.r_handler, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True,
                     script_from_db=True,
                     script_name="absolute_dotted_chart"),

            e_object(intent="Dottedchart_relative_follow",
                     function=pm.r_handler, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True,
                     script_from_db=True,
                     script_name="relative_dotted_chart"), #TO BE IMPLEMENTED

            e_object(intent="Dottedchart_absolute",
                     command="/dottedchartabsolute",
                     command_help="Creates an absolute dotted chart for the current log", 
                     function=pm.r_handler, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True,
                     script_from_db=True,
                     script_name="absolute_dotted_chart"), #TO BE IMPLEMENTED

            e_object(intent="Dottedchart_relative",
                     command="/dottedchartrelative", 
                     command_help="Creates a relative dotted chart for the current log", 
                     function=pm.r_handler, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True,
                     script_from_db=True,
                     script_name="relative_dotted_chart"), #TO BE IMPLEMENTED

            e_object(intent="Fine",
                     function="That's nice to hear!",
                     reply_type=ReplyType.text),

            e_object(intent="Help",
                     command="/help", 
                     command_help="Shows the help menu", 
                     function=execution.get_help_text, 
                     execution=Execution.Nothing, 
                     reply_type=ReplyType.text),

            e_object(intent="HowAreYou",
                     function="I am fine and you?",
                     reply_type=ReplyType.text),

            e_object(intent="Inductive",
                     command="/inductive", 
                     command_help="Does the inductive miner on the current log", 
                     function=pm.do_inductive_miner, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True),

            e_object(intent="List_chat_files",
                     command="/list", 
                     command_help="Lists the files currently available in this chat", 
                     function=context_manager.list_chat_files, 
                     execution=Execution.Chat_id, 
                     reply_type=ReplyType.text,
                     change_state=True,
                     new_state=BotState.Listing_files),

            e_object(intent="Mining",
                     function="pass",
                     reply_type=ReplyType.text), #TO BE IMPLEMENTED

            e_object(intent="No",
                     function="pass",
                     reply_type=ReplyType.text), #TO BE IMPLEMENTED

            e_object(intent="PrecedenceMatrix",
                     command="/precedencematrix", 
                     command_help="Creates a precedence matrix for the current log", 
                     function=pm.r_handler, 
                     execution=Execution.Log, 
                     reply_type=ReplyType.photo, 
                     ask_for_file= True,
                     script_from_db=True,
                     script_name="precedence_matrix"), #TO BE IMPLEMENTED

            e_object(intent="Sad",
                     function="I'm sorry to hear that. What's the problem?",
                     reply_type=ReplyType.text),

            e_object(intent="Show_resources",
                     command="/resources", 
                     command_help="Shows the current resources", 
                     function="pass", 
                     execution=Execution.Log, 
                     reply_type="", 
                     ask_for_file= True), #TO BE IMPLEMENTED SHOW MIMIC (SHOWRESOURCES FROM PMBOT)
                     
            e_object(intent="Welcome",
                     function="Hi user! nice to meet you!",
                     reply_type=ReplyType.text),
                     
            e_object(intent="Yes",
                     function="pass",
                     reply_type=ReplyType.text) #TO BE IMPLEMENTED
        ]
