import subprocess
import tempfile

def inductive(prom_lite):
    new_file, script_file = tempfile.mkstemp()
    new_file, pic_file = tempfile.mkstemp(suffix="png")
    subprocess.run("ProMLite12.bat")
    print(script_file)
    print(pic_file)
    with open(script_file, "w+") as f:
        f.write(get_executor_script(0, pic_file))
    subprocess.run([prom_lite, "-f", script_file])
    return pic_file

def get_executor_script(chat_id, pic_filename):
    return """log = open_xes_log_file("LOG_FILE");
org.processmining.plugins.InductiveMiner.mining.MiningParameters params = new org.processmining.plugins.InductiveMiner.mining.MiningParametersIMf();
org.processmining.processtree.ProcessTree tree = mine_process_tree_with_inductive_miner_with_parameters(log, params);
javax.swing.JComponent component = process_tree_visualisation_inductive_visual_miner_(tree);
org.processmining.plugins.graphviz.dot.Dot d = ((org.processmining.plugins.graphviz.visualisation.DotPanel) component).getDot();
export_dot_as_png(d, new File("PIC_FILE"));
System.exit(0);""".replace("LOG_FILE", r"C:\Users\Rasmu\OneDrive\School\Thesis\Python\firstLog.xes").replace("PIC_FILE", pic_filename).replace("\\", "\\\\")

prom = r"C:\Users\Rasmu\ProM Lite 1.2\ProMLite12.bat"
prom2 = r"C:\Users\Rasmu\OneDrive\School\Thesis\Python\ProMLite12.bat"
inductive(prom2)