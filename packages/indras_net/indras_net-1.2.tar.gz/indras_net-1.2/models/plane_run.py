#!/usr/bin/env python3
"""
A script to test our spatial capabilities on the complex plane.
"""

import indra.utils as utils
import indra.prop_args as props
import indra.plane_env as pe
import plane_model as pm

# set up some file names:
MODEL_NM = "spatial_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("num_agents", 2)

# Now we create a minimal environment for our agents to act within:
env = pe.PlaneEnv("Test plane env", 100.0, 100.0, model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(
        pm.TestPlaneAgent(name="agent" + str(i),
                          goal="moving around aimlessly!"))

utils.run_model(env, prog_file, results_file)
