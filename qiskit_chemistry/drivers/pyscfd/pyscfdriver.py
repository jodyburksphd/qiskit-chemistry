# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from qiskit_chemistry.drivers import BaseDriver
from qiskit_chemistry import QiskitChemistryError
from qiskit_chemistry.drivers.pyscfd.integrals import compute_integrals
import importlib
import logging

logger = logging.getLogger(__name__)


class PySCFDriver(BaseDriver):
    """Python implementation of a PySCF driver."""

    CONFIGURATION = {
        "name": "PYSCF",
        "description": "PYSCF Driver",
        "input_schema": {
            "$schema": "http://json-schema.org/schema#",
            "id": "pyscf_schema",
            "type": "object",
            "properties": {
                "atom": {
                    "type": "string",
                    "default": "H 0.0 0.0 0.0; H 0.0 0.0 0.735"
                },
                "unit": {
                    "type": "string",
                    "default": "Angstrom",
                    "oneOf": [
                        {"enum": ["Angstrom", "Bohr"]}
                    ]
                },
                "charge": {
                    "type": "integer",
                    "default": 0
                },
                "spin": {
                    "type": "integer",
                    "default": 0
                },
                "basis": {
                    "type": "string",
                    "default": "sto3g"
                },
                "max_memory": {
                    "type": ["integer", "null"],
                    "default": None
                }
            },
            "additionalProperties": False
        }
    }

    def __init__(self):
        super().__init__()

    @staticmethod
    def check_driver_valid():
        err_msg = "PySCF is not installed. Use 'pip install pyscf'"
        try:
            spec = importlib.util.find_spec('pyscf')
            if spec is not None:
                return
        except Exception as e:
            logger.debug('PySCF check error {}'.format(str(e)))
            raise QiskitChemistryError(err_msg) from e

        raise QiskitChemistryError(err_msg)

    def run(self, section):
        return compute_integrals(section['properties'])
