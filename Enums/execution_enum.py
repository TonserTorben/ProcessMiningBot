import enum

class ExecutionState(enum.Enum):
    Log                     = 1
    Model                   = 2
    Both                    = 3
    Nothing                 = 4
    Chat_id                 = 5
    Alpha                   = 19
    Conformance_Complete    = 6
    Conformance_Fitness     = 7
    Conformance_Precision   = 8
    Description             = 9
    Dfg_Resource            = 10
    Dfg_Performance         = 11
    Dottedchart_Absolute    = 12
    Dottedchart_Relative    = 13
    Help                    = 14
    Inductive               = 15
    Precedencematrix        = 16
    Resources               = 17
    ListFiles               = 18
