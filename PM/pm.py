import os
import tempfile
import pm4py
import Globals

from PM import rexecutor as r_exe

from pm4py.util                                         import constants

from pm4py.objects.log                                  import util
from pm4py.objects.log.importer.xes                     import factory as xes_import_factory
from pm4py.objects.log.exporter.xes                     import factory as xes_exporter
from pm4py.objects.petri.importer                       import pnml as pnml_importer
from pm4py.objects.petri.exporter                       import pnml as pnml_exporter

from pm4py.objects.conversion.log                       import factory as conversion_factory

from pm4py.visualization.petrinet                       import factory as pn_vis_factory
from pm4py.visualization.dfg                            import factory as dfg_vis_factory
from pm4py.visualization.graphs                         import factory as graphs_vis_factory

from pm4py.evaluation                                   import factory as evaluation_factory
from pm4py.evaluation.replay_fitness                    import factory as replay_factory
from pm4py.evaluation.precision                         import factory as precision_factory

from pm4py.algo.discovery.alpha                         import factory as alpha_miner
from pm4py.algo.discovery.inductive                     import factory as inductive_miner
from pm4py.algo.discovery.dfg                           import factory as dfg_factory

from pm4py.algo.conformance.alignments                  import factory as align_factory
from pm4py.algo.conformance.tokenreplay                 import factory as token_based_replay
from pm4py.algo.conformance.tokenreplay.diagnostics     import duration_diagnostics

from pm4py.algo.filtering.log.auto_filter.auto_filter   import apply_auto_filter
from pm4py.algo.filtering.log.attributes                import attributes_filter
from pm4py.algo.filtering.log.start_activities          import start_activities_filter
from pm4py.algo.filtering.log.end_activities            import end_activities_filter

from pm4py.statistics.traces.log                        import case_statistics

def import_log(log):
    return xes_import_factory.import_log(log)

def import_model(model):
    return pnml_importer.import_net(model)

def show_model(model):
    net, initial_marking, final_marking = import_model(model)
    gvis = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gvis, file_name)
    return file_name

#Alpha Miner
def do_alpha_miner(log):
    log = import_log(log)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gviz, file_name)
    return file_name

#Inductive Miner
def do_inductive_miner(log):
    log = import_log(log)
    net, initial_marking, final_marking = inductive_miner.apply(log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gviz, file_name)
    return file_name

#Directed flow graph if performance then performance=True
def do_dfg_performance(log):
    log = import_log(log)
    dfg = dfg_factory.apply(log) 
    gviz = dfg_vis_factory.apply(dfg, log=log, variant="performance")    
    _, file_name = tempfile.mkstemp(suffix='.png')
    dfg_vis_factory.save(gviz, file_name)
    return file_name

def do_dfg_resource(log):
    log = import_log(log)
    dfg = dfg_factory.apply(log) 
    gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")
    _, file_name = tempfile.mkstemp(suffix='.png')
    dfg_vis_factory.save(gviz, file_name)
    return file_name

#Describe log !! DOESN'T WORK!!!
def log_desciption(log):
    log = import_log(log)
    file_1 = None
    file_2 = None
    #duration
    try:
        x, y = case_statistics.get_kde_caseduration(log, parameters={constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"})
        gviz = graphs_vis_factory.apply_plot(x, y, variant="cases")
        _, file_1 = tempfile.mkstemp(suffix=".png")
        graphs_vis_factory.save(gviz, file_1)
    except OSError: 
        pass
    #over time
    try: 
        x, y = attributes_filter.get_kde_date_attribute(log, attribute="time:timestamp")
        gviz2 = graphs_vis_factory.apply_plot(x, y, variant="dates")
        _, file_2 = tempfile.mkstemp(suffix=".png")
        graphs_vis_factory.save(gviz2, file_2)
    except OSError as e:
        print("error when calcing over time")
        print(e)
    
    result = {"traces"            : len(log), 
            "acts_freq"         : util.log.get_event_labels_counted(log, "concept:name"),
            "case_duration"     : file_1,
            "events_over_time"  : file_2}
    print(file_1)
    return result

#Filtering Section
#get activities of log
def get_activities(log):
    log = import_log(log)
    return util.log.get_event_labels(log, "concept:name")

def get_start_activities(log):
    log = import_log(log)
    return start_activities_filter.get_start_activities(log)

def get_end_activities(log):
    log = import_log(log)
    return end_activities_filter.get_end_activities(log)

#Apply filter for keeping activities
def filter_keep_activities(log, activities):
    log = import_log(log)
    tracefilter_log_pos = attributes_filter.apply_events(log, activities, parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "concept:name", "positive": True})
    _, temp_file = tempfile.mkstemp(suffix='.png')
    xes_exporter.export_log(tracefilter_log_pos, temp_file, parameters={"compress": False})
    return temp_file
    
def filter_start_activities(log, activities):
    log = import_log(log)
    filtered_log = start_activities_filter.apply(log, activities)
    _, temp_file = tempfile.mkstemp(suffix='.png')
    xes_exporter.export_log(filtered_log, temp_file, parameters={"compress": False})

def filter_end_activities(log, activities):
    log = import_log(log)
    filtered_log = end_activities_filter.apply(log, activities)
    _, temp_file = tempfile.mkstemp(suffix='.png')
    xes_exporter.export_log(filtered_log, temp_file, parameters={'compress': False})


#Conformance Section
def do_conformance(log, model, conformance_type, model_type):
    if conformance_type == 'fitness':
        return conformance_fitness(log, model, model_type)
    elif conformance_type == 'precision':
        return conformance_precision(log, model, model_type)
    elif conformance_type == 'complete':
        return conformance_complete(log, model, model_type)

def conformance_fitness(log, model, model_type):
    log = import_log(log)
    if model_type == 'alpha':
        net, initial_marking, final_marking = alpha_miner.apply(log)
    elif model_type == 'inductive':
        net, initial_marking, final_marking = inductive_miner.apply(log)
    elif model_type == 'current':
        net, initial_marking, final_marking = import_model(model)

    fitness = replay_factory.apply(log, net, initial_marking, final_marking)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gviz, file_name)
    return {'result': fitness, 
            'Model': file_name}

def conformance_precision(log, model, model_type):
    log = import_log(log)
    if model_type == 'alpha':
        net, initial_marking, final_marking = alpha_miner.apply(log)
    elif model_type == 'inductive':
        net, initial_marking, final_marking = inductive_miner.apply(log)
    elif model_type == 'current':
        net, initial_marking, final_marking = import_model(model)
    
    precision = precision_factory.apply(log, net, initial_marking, final_marking)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gviz, file_name)
    return {'result': precision,
            'Model': file_name}

def conformance_complete(log, model, model_type):
    log = import_log(log)
    if model_type == 'alpha':
        net, initial_marking, final_marking = alpha_miner.apply(log)
    elif model_type == 'inductive':
        net, initial_marking, final_marking = inductive_miner.apply(log)
    elif model_type == 'current':
        net, initial_marking, final_marking = import_model(model)
    
    evaluation = evaluation_factory.apply(log, net, initial_marking, final_marking)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='.png')
    pn_vis_factory.save(gviz, file_name)
    return {'result': evaluation,
            'Model': file_name}

def r_handler(script, log):
    r_script = Globals.get_r_script()
    _, script_file = tempfile.mkstemp()
    with open(script_file, "w+") as f:
        f.write(script)
    return r_exe.run_r(r_script, script_file, log)