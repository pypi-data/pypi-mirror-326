import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXECUTABLE_DIR = os.path.join(ROOT_DIR, "executables")
SAMPLES_DIR = os.path.join(ROOT_DIR, "samples")
ROSETTA_DIR = os.path.join(ROOT_DIR, "rosetta3")
TMP_DIR = os.path.join(ROOT_DIR, "tmp")

DMWEA_EXEC = os.path.join(EXECUTABLE_DIR, "DMWEA.EXE")
DMSOILP_EXEC = os.path.join(EXECUTABLE_DIR, "DMSOILP.EXE")

GEN_FILE = os.path.join(SAMPLES_DIR, "LenaweeCoMI.gen")


