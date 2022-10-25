#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger("pre_gen_project")


MODULE_REGEX = r"^[a-z][_a-z0-9]+$"
PROJECT_REGEX = r"^[a-zA-Z][\-_a-zA-Z0-9]+$"

module_name = "{{cookiecutter.package_name}}"
project_name = "{{cookiecutter.project_name}}"

if not re.match(MODULE_REGEX, module_name):
    link = "https://www.python.org/dev/peps/pep-0008/#package-and-module-names"
    logger.error("Module name should be pep-8 compliant.")
    logger.error("  More info: {}".format(link))
    sys.exit(1)

if not re.match(PROJECT_REGEX, project_name):
    logger.error("Project name should contain only alphanumeric and '_' or '-' characters.")
    sys.exit(1)
