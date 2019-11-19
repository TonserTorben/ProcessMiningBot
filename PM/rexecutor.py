import subprocess
import tempfile

def run_r(r_script, scriptname, log):
    _, tmp_filename = tempfile.mkstemp(suffix='png')
    subprocess.run([r_script,
                    scriptname,
                    log,
                    tmp_filename])
    return tmp_filename