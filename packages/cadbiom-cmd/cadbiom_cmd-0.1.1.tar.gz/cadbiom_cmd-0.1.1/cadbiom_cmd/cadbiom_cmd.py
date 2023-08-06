# -*- coding: utf-8 -*-
# Copyright (C) 2017  IRISA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original code contained here was initially developed by:
#
#     Pierre Vignet.
#     IRISA
#     Dyliss team
#     IRISA Campus de Beaulieu
#     35042 RENNES Cedex, FRANCE
from __future__ import unicode_literals
from __future__ import print_function

# Standard imports
import argparse
import os

# Custom imports
import cadbiom.commons as cm

LOGGER = cm.logger()

def launch_researchs(args):
    """Parse arguments and launch Cadbiom search of MACs
    (Minimal Activation Conditions).

    - If there is no input file, there will be only one process.
    - If an input file is given, there will be 1 process per line (per logical
    formula on each line).
    - all_macs: Solver will try to search all macs with 0 to
    the maximum of steps allowed.
    - continue: If there is a mac file from a previous work, last frontier
    places will be reloaded.
    """

    # Module import
    import solution_search
    params = args_to_param(args)
    solution_search.launch_researchs(params) # !


def launch_sort(args):
    """Parse a solution file and sort all frontier places in alphabetical order.
    """

    # Module import
    import solution_sort
    params = args_to_param(args)
    solution_sort.sort_solutions(params['sol_file'])


def parse_trajectories(args):
    """Parse a complete solution file and make a representation of trajectories.

    The output is in graphml file format and is exported in 'graphs' directory.

    .. note:: Requires the model file.
    """

    # Module import
    import solution_repr
    params = args_to_param(args)
    params['output'] = params['output'] if params['output'][-1] == '/' \
                        else params['output'] + '/'
    solution_repr.main(
        params['output'],
        params['chart_file'],
        params['sol_file']
    )


def model_comp(args):
    """Model consistency checking.

    Check if the 2 given models have the same topology,
    nodes & edges attributes/roles.

    .. note:: You can export a graphml file for the 2 models.
    """

    # Module import
    import solution_repr
    params = args_to_param(args)
    params['output'] = params['output'] if params['output'][-1] == '/' \
                        else params['output'] + '/'
    solution_repr.graph_isomorph_test(
        params['model_file_1'],
        params['model_file_2'],
        params['output'],
        params['graphs'],
        params['json'],
    )


def model_infos(args):
    """Model informations.

    Get number of nodes, edges, centralities (degree, closeness, betweenness).

    .. note:: You can export a graphml file for model.
    """

    # Module import
    import solution_repr
    params = args_to_param(args)
    params['output'] = params['output'] if params['output'][-1] == '/' \
                        else params['output'] + '/'
    solution_repr.graph_infos(
        params['model_file'],
        params['output'],
        params['graph'],
        params['json'],
        params['advanced'],
    )


def merge_cams(args):
    """Merge solutions to a csv file.

    .. note:: CSV file: <Final property formula>;<cam>
    """

    # Module import
    import solution_merge
    params = args_to_param(args)
    solution_merge.merge_cams_to_csv(params['solutions_directory'],
                                     params['output'])


def args_to_param(args):
    """Return argparse namespace as a dict {variable name: value}"""
    return {k: v for k, v in vars(args).items() if k != 'func'}


class ReadableFile(argparse.Action):
    """
    http://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
    """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_file = values

        if not os.path.isfile(prospective_file):
            raise argparse.ArgumentTypeError(
                "readable_file:{0} is not a valid path".format(
                    prospective_file)
                )

        if os.access(prospective_file, os.R_OK):
            setattr(namespace, self.dest, prospective_file)
        else:
            raise argparse.ArgumentTypeError(
                "readable_file:{0} is not a readable file".format(
                    prospective_file)
                )


class ReadableDir(argparse.Action):
    """
    http://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
    """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                "readable_dir:{0} is not a valid path".format(
                    prospective_dir)
                )

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                "readable_dir:{0} is not a readable dir".format(
                    prospective_dir)
                )


def main():

    # parser configuration
    parser = argparse.ArgumentParser(description=__doc__)
    # Default log level: debug
    parser.add_argument('-vv', '--verbose', nargs='?', default='info')
    # Subparsers
    subparsers = parser.add_subparsers(title='subcommands')

    # PS: nargs='?' = optional
    # subparser: Compute macs
    #    steps      = 10
    #    final_prop = "P"
    #    start_prop = None
    #    inv_prop   = None
    parser_input_file = subparsers.add_parser('compute_macs',
                                              help=launch_researchs.__doc__)
    parser_input_file.add_argument('chart_file')
#    parser_input_file.add_argument('final_prop')
    # Get final_property alone OR an input_file containing multiple properties
    group = parser_input_file.add_mutually_exclusive_group()
    group.add_argument('final_prop', nargs='?')
    group.add_argument('--input_file', action=ReadableFile, nargs='?')
    # If input_file is set, we can compute all combinations of given elements
    # default: False
    parser_input_file.add_argument('--combinations', action='store_true')
    parser_input_file.add_argument('--steps', type=int, nargs='?', default=10)
    # https://docs.python.org/dev/library/argparse.html#action
    # all_macs to False by default
    parser_input_file.add_argument('--all_macs', action='store_true')
    # continue to False by default
    parser_input_file.add_argument('--continue', action='store_true')
    parser_input_file.add_argument('--start_prop', nargs='?', default=None)
    parser_input_file.add_argument('--inv_prop', nargs='?', default=None)
    parser_input_file.add_argument('--output', action=ReadableDir, nargs='?',
                                   default='result/')
    parser_input_file.set_defaults(func=launch_researchs)


    # subparser: Sort solutions in alphabetical order in place
    # Solution file (complete or not)
    parser_solutions_sort = subparsers.add_parser('sort_solutions',
                                                  help=launch_sort.__doc__)
    parser_solutions_sort.add_argument('sol_file')
    parser_solutions_sort.set_defaults(func=launch_sort)


    # subparser: Representation of the trajectories of MACs in a complete file.
    # Model file (xml : cadbiom language)
    # Solution file (cam_complete)
    parser_trajectories = subparsers.add_parser('parse_trajectories',
                                                help=parse_trajectories.__doc__)
    parser_trajectories.add_argument('chart_file')
    parser_trajectories.add_argument('sol_file')
    parser_trajectories.add_argument('--output', action=ReadableDir,
                                     nargs='?', default='graphs/')
    parser_trajectories.set_defaults(func=parse_trajectories)


    # subparser: Merge solutions to a csv file
    # Solution file (cam)
    # Output (csv)
    parser_merge_cams = subparsers.add_parser('merge_cams',
                                              help=merge_cams.__doc__)
    parser_merge_cams.add_argument('solutions_directory', nargs='?',
                                   default='result/')
    parser_merge_cams.add_argument('--output', nargs='?',
                                   default='result/merged_cams.csv')
    parser_merge_cams.set_defaults(func=merge_cams)


    # subparser: Model comparison
    # 2 models
    parser_model_comparison = subparsers.add_parser('model_comp',
                                                    help=model_comp.__doc__)
    parser_model_comparison.add_argument('model_file_1')
    parser_model_comparison.add_argument('model_file_2')
    # Export graphs for the 2 models; default: false
    parser_model_comparison.add_argument('--graphs', action='store_true')
    parser_model_comparison.add_argument('--json', action='store_true')
    parser_model_comparison.add_argument('--output', action=ReadableDir,
                                         nargs='?', default='graphs/')
    parser_model_comparison.set_defaults(func=model_comp)


    # subparser: Model infos
    # 1 model
    parser_model_infos = subparsers.add_parser('model_infos',
                                                    help=model_infos.__doc__)
    parser_model_infos.add_argument('model_file')
    # Export graphs for the 2 models; default: false
    parser_model_infos.add_argument('--graph', action='store_true')
    parser_model_infos.add_argument('--json', action='store_true')
    parser_model_infos.add_argument('--advanced', action='store_true')
    parser_model_infos.add_argument('--output', action=ReadableDir,
                                    nargs='?', default='graphs/')
    parser_model_infos.set_defaults(func=model_infos)


    # get program args and launch associated command
    args = parser.parse_args()

    # Set log level
    cm.log_level(vars(args)['verbose'])

    # launch associated command
    args.func(args)
