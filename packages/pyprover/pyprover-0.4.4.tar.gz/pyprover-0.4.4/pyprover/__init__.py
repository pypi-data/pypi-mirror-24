#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x637dda57

# Compiled with Coconut version 1.2.3-post_dev40 [Colonel]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.abspath(__file__))
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import _coconut, _coconut_NamedTuple, _coconut_MatchError, _coconut_tail_call, _coconut_tco, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_pipe, _coconut_star_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial
from __coconut__ import *
_coconut_sys.path.remove(_coconut_file_path)

# Compiled Coconut: -----------------------------------------------------------

# Imports:

from pyprover.logic import ForAll
from pyprover.logic import Exists
from pyprover.logic import FA
from pyprover.logic import TE
from pyprover.logic import top
from pyprover.logic import bot
from pyprover.logic import true
from pyprover.logic import false
from pyprover.logic import Not
from pyprover.logic import Imp
from pyprover.logic import Or
from pyprover.logic import And
from pyprover.logic import Eq
from pyprover.tools import props
from pyprover.tools import terms
from pyprover.tools import solve
from pyprover.tools import strict_solve
from pyprover.tools import no_proof_of
from pyprover.tools import proves
from pyprover.tools import strict_proves
from pyprover.tools import proves_and_proved_by
from pyprover.tools import strict_proves_and_proved_by
from pyprover.tools import iff
from pyprover.tools import simplify
from pyprover.tools import strict_simplify
from pyprover.tools import simplest_form
from pyprover.tools import strict_simplest_form
from pyprover.tools import simplest_solution
from pyprover.tools import strict_simplest_solution
from pyprover.tools import substitute
from pyprover.atoms import LowercasePropositions
from pyprover.atoms import UppercasePropositions
from pyprover.atoms import LowercaseVariables
from pyprover.atoms import UppercaseVariables
from pyprover.atoms import StandardMath
from pyprover.parser import expr

# Main:

StandardMath.use(globals())
