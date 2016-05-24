# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines workflows for vasp calculations that require structure transformations.
"""

from fireworks import Workflow
import os
from pymatgen.io.vasp.sets import MPVaspInputSet

from monty.serialization import loadfn
from matmethods.utils.loaders import get_wf_from_spec_dict

__author__ = 'Kiran Mathew'
__email__ = 'kmathew@lbl.gov'


def get_wf_transmuter(structure, vasp_input_set=None, vasp_cmd="vasp", db_file=None):
    """
    Return vasp workflow consisting of 2 fireworks:

    Firework 1 : write vasp input set for structural relaxation,
                 run vasp,
                 pass run location,
                 database insertion.

    Firework 2 : copy files from previous run,
                 apply the transformations and write vasp input set,
                 run vasp,
                 pass run location
                 database insertion.

    Args:
        structure (Structure): input structure to be optimized and run
        vasp_input_set (DictVaspInputSet): vasp input set.
        vasp_cmd (str): command to run
        db_file (str): path to file containing the database credentials.

    Returns:
        Workflow
    """
    d = loadfn(os.path.join(os.path.dirname(__file__), "transmuter.yaml"))

    v = vasp_input_set or MPVaspInputSet(force_gamma=True)
    d["fireworks"][0]["params"] = {"vasp_input_set": v.as_dict()}

    d["common_params"] = {
        "vasp_cmd": vasp_cmd,
        "db_file": db_file
    }

    return get_wf_from_spec_dict(structure, d)


# Note to others: You can always write your tests in the same file for a start.
# This way, when you are ready, you simply copy this to a new file.
# Instead of writing a main method.
# It is not that much longer, especially if you have test snippets stored in a
# text replacement program like me. -- Hulk
from pymatgen.util.testing import PymatgenTest

class FuncTest(PymatgenTest):

    def test_get_wf_transmuter(self):
        # Should replace with proper test.
        structure = PymatgenTest.get_structure("Si")
        wf = get_wf_transmuter(structure)