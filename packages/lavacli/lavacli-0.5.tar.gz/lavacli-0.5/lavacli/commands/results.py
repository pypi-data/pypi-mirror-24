# -*- coding: utf-8 -*-
# vim: set ts=4

# Copyright 2017 Rémi Duraffort
# This file is part of lavacli.
#
# lavacli is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lavacli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with lavacli.  If not, see <http://www.gnu.org/licenses/>

import sys
import yaml


def configure_parser(parser):
    parser.add_argument("job_id", help="job id")
    parser.add_argument("test_suite", nargs="?", default=None, help="test suite")
    parser.add_argument("test_case", nargs="?", default=None, help="test case")
    parser.add_argument("--yaml", dest="output_format", default=None,
                        action="store_const", const="yaml",
                        help="print as yaml")


def help_string():
    return "manage results"


def handle(proxy, options, _):
    if options.test_case is not None:
        data = proxy.results.get_testcase_results_yaml(options.job_id,
                                                       options.test_suite,
                                                       options.test_case)
    elif options.test_suite is not None:
        data = proxy.results.get_testsuite_results_yaml(options.job_id,
                                                        options.test_suite)
    else:
        data = proxy.results.get_testjob_results_yaml(options.job_id)

    results = yaml.load(data)

    if options.output_format == "yaml":
        print(yaml.dump(results).rstrip("\n"))
    else:
        # Only one to print
        if options.test_case is not None:
            res = results[0]
            if not sys.stdout.isatty():
                print("%s" % res["result"])
            elif res["result"] == "pass":
                print("\033[1;32mpass\033[0m")
            elif res["result"] == "fail":
                print("\033[1;31mfail\033[0m")
            else:
                print("%s" % res["result"])
        # A list to print
        else:
            print("Results:")
            for res in results:
                if not sys.stdout.isatty():
                    print("* %s.%s [%s]" % (res["suite"], res["name"], res["result"]))
                elif res["result"] == "pass":
                    print("* %s.%s [\033[1;32mpass\033[0m]" % (res["suite"], res["name"]))
                elif res["result"] == "fail":
                    print("* %s.%s [\033[1;31mfail\033[0m]" % (res["suite"], res["name"]))
                else:
                    print("* %s.%s [%s]" % (res["suite"], res["name"], res["result"]))
