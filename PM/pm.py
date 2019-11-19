import os
import tempfile
import pm4py

from pm4py.util import constants

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.log import util

from pm4py.objects.conversion.log   import factory as conversion_factory

from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory
from pm4py.visualization.graphs import factory as graphs_vis_factory

from pm4py.evaluation.replay_fitness import factory as replay_fitness_factory

from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.discovery.dfg import factory as dfg_factory

from pm4py.algo.conformance.alignments import factory as align_factory
from pm4py.algo.conformance.tokenreplay import factory as token_based_replay
from pm4py.algo.conformance.tokenreplay.diagnostics import duration_diagnostics

from pm4py.algo.filtering.log.auto_filter.auto_filter import apply_auto_filter
from pm4py.algo.filtering.log.attributes import attributes_filter

from pm4py.statistics.traces.log import case_statistics

#log = xes_import_factory.apply(os.path.join("log1.xes"))

#Alpha Miner
def do_alpha_miner(log):
    log = xes_import_factory.apply(log)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    _, file_name = tempfile.mkstemp(suffix='png')
    pn_vis_factory.save(gviz, file_name)
    return file_name

#Directed flow graph if performance
def do_dfg(log, performance):
    if performance: 
        dfg = dfg_factory.apply(log, variant="performance")
        gviz = dfg_vis_factory.apply(dfg, log=log, variant="performance")
    else: 
        dfg = dfg_factory.apply(log)
        gviz = dfg_vis_factory.apply(dfg, log=log, variant="frequency")
    _, file_name = tempfile.mkstemp(suffix='png')
    dfg_vis_factory.save(gviz, file_name)
    return file_name

#Describe log
def log_desciption(log):
    file_1 = None
    file_2 = None
    #duration
    try:
        x, y = case_statistics.get_kde_caseduration(log, parameters={constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"})
        gviz = graphs_vis_factory.apply_plot(x, y, variant="cases")
        _, file_1 = tempfile.mkstemp(suffix="png")
        graphs_vis_factory.save(gviz, file_1)
    except OSError: 
        pass
    #over time
    try: 
        x, y = attributes_filter.get_kde_date_attribute(log, attribute="time:timestamp")
        gviz2 = graphs_vis_factory.apply_plot(x, y, variant="dates")
        _, file_2 = tempfile.mkstemp(suffix="png")
        graphs_vis_factory.save(gviz2, file_2)
    except OSError:
        pass

    return {"traces": len(log), 
            "acts_freq": util.log.get_event_labels_counted(log, "concept:name"),
            "case_duration": file_1,
            "events_over_time": file_2}

#get activities of log
def get_activities(log):
    return util.log.get_event_labels(log, "concept:name")

#Filtering

def filer_keep_activities(log, activities):
    tracefilter_log_pos = attributes_filter.apply_events(log, activities, parameters={constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY: "concept:name", "positive": True})
    xes_exporter.export_log(tracefilter_log_pos, os.path.join(log, "_filtered.xes"), parameters={"compress": False})
    

from pm4py.evaluation.replay_fitness import factory as replay_factory
from pm4py.objects.petri.importer import pnml as pnml_importer
from pm4py.objects.petri.exporter import pnml as pnml_exporter

def conformance_fitness():
    log = xes_import_factory.import_log(os.path.join("Files", "Test_1_log_no_compress.xes"))
    net, initial_marking, final_marking = pnml_importer.import_net(os.path.join("Files", "Petrinet_test_1.pnml"))
    alpha_petri, alpha_initial_marker, alpha_final_marker = alpha_miner.apply(log)
    inductive_petri, inductive_initial_marker, inductive_final_marker = inductive_miner.apply(log)
    gviz = pn_vis_factory.apply(alpha_petri, alpha_initial_marker, alpha_final_marker)
    gviz2 = pn_vis_factory.apply(inductive_petri, inductive_initial_marker, inductive_final_marker)
    gviz3 = pn_vis_factory.apply(net, initial_marking, final_marking)
    pn_vis_factory.view(gviz)
    pn_vis_factory.view(gviz2)
    pn_vis_factory.view(gviz3)
    pnml_exporter.export_net(net, initial_marking, "petrinet.pnml")
    fitness_alpha = replay_factory.apply(log, alpha_petri, alpha_initial_marker, alpha_final_marker)
    fitness_inductive = replay_factory.apply(log, inductive_petri, inductive_initial_marker, inductive_final_marker)
    fitness = replay_factory.apply(log, net, initial_marking, final_marking)
    print("fitness_alpha=", fitness_alpha)
    print("fitness_inductive=", fitness_inductive)
    print("total fitness=", fitness)

#conformance_fitness()