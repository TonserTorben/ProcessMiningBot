import subprocess
import tempfile
import os
from PIL import Image

from decouple import config

script = config("R_SCRIPT")

def dotted_chart():
    pic = run_r_code(script, "R/dottedchart.R", "firstlog.xes", "", "")
    #Create file if not exists and write png file
    f = open('test.png', 'wb')
    chart =  open(pic, 'rb')
    f.write(chart.read())
    f.close()
    #Open file directly
    #os.startfile(pic)


def run_r_code(r_script, filename, log, r_type, start):
    new_file, tmp_filename = tempfile.mkstemp(suffix="png")
    subprocess.run([r_script,
                    filename,
                    log,
                    tmp_filename,
                    r_type,
                    start])
    return tmp_filename

def uni_chart():
    pic = run_r_code(script, "R/uni_dotted_chart.R", "firstlog.xes", "relative", "duration")
    f = open('test2.png', 'wb')
    chart = open(pic, 'rb')
    f.write(chart.read())
    f.close()

dotted_chart()
uni_chart()