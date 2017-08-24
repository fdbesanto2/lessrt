#coding: utf-8
from session import session
import os
import subprocess
from FileHelper import *
from Constant import current_rt_program
import math

def convert_obj_2_serialized(inputobjpath, outputserilizeddir):
    currdir = os.path.split(os.path.realpath(__file__))[0]
    os.environ['PATH'] = currdir + '/bin/rt/'+ current_rt_program +'/' + os.pathsep + os.environ['PATH']
    (filepath, tempfilename) = os.path.split(inputobjpath)
    xmlfilename = os.path.splitext(tempfilename)[0]
    outputserilizedpath = combine_file_path(outputserilizeddir, xmlfilename)
    # cmd = "mtsimport " + inputobjpath +" " + outputserilizedpath
    log("INFO: Converting "+ os.path.basename(inputobjpath) + " to binary format.")
    if os.path.exists(outputserilizedpath+".serialized"):
        log("INFO: Using cached file.")
        return
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['mtsimport', inputobjpath.encode("utf-8"), outputserilizedpath.encode("utf-8")], stdout=devnull, stderr=subprocess.STDOUT)
    # os.system(cmd)
    shutil.rmtree(combine_file_path(os.getcwd(),"textures"))
    xmlfile = combine_file_path(outputserilizeddir,xmlfilename)
    os.remove(xmlfile)

def isDigitNum(numstr):
    numstr = numstr.replace('.', '', 1)
    return numstr.isdigit()


# for example 0,0,0,0
def check_if_string_is_zero_and_comma(valueof):
    arr = valueof.split(",")
    for i in range(0, len(arr)):
        if float(arr[i]) != 0:
            return False
    return True

# planck law at wavelength nm  w/m^2/sr/nm
def planck_law_fun(temperature, wavelength):
    kb = 1.38064852e-23  # Boltzmann constant
    hp = 6.626070040e-34  # Planck constant
    c = 299792458
    wavelength *= math.pow(10,-9)
    down = math.exp(hp*c/(wavelength*kb*temperature))-1
    radiance = 2*hp*c*c/(math.pow(wavelength,5))*1.0/(down)
    return radiance*math.pow(10,-9)

# planck定律计算每个波段的radiance
def emittion_spectral(temperature, lamdbda_list):
    delta = 1  # nm
    wlArr = lamdbda_list.split(",")
    spectral = ""
    for wl in wlArr:
        wbarr = wl.split(":")
        w, b = float(wbarr[0]), float(wbarr[1])
        lambda_min,lambda_max = w-0.5*b, w+0.5*b
        integral_num= int(math.ceil(b))
        ingegral = 0
        for i in range(0, integral_num):
            lambdaleft = min(lambda_min + i * delta,lambda_max)
            lambdaright = min(lambda_min + (i + 1) * delta,lambda_max)
            ingegral += (planck_law_fun(temperature, lambdaleft) + planck_law_fun(temperature, lambdaright)) * delta  / 2.0
        radiance = ingegral/b
        spectral += str(radiance) + ","
    return spectral[0:len(spectral)-1]

