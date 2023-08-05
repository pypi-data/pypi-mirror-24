import os
import sys
import argparse
import platform

from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec

from molotov.fmwk import runner
from molotov.api import get_scenarios, get_scenario
from molotov import __version__
from molotov.util import log, expand_options, OptionError
from molotov import ui


PYPY = platform.python_implementation() == 'PyPy'


def _parser():
    parser = argparse.ArgumentParser(description='Load test.')

    parser.add_argument('scenario', default="loadtest.py",
                        help="path or module name that contains scenarii",
                        nargs="?")

    parser.add_argument('-s', '--single-mode', default=None, type=str,
                        help="Name of a single scenario to run once.")

    parser.add_argument('--config', default=None, type=str,
                        help='Point to a JSON config file.')

    parser.add_argument('--version', action='store_true', default=False,
                        help='Displays version and exits.')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Run the event loop in debug mode.')

    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help=('Verbosity level. -v will display '
                              'tracebacks. -vv requests and responses.'))

    parser.add_argument('-w', '--workers', help='Number of workers',
                        type=int, default=1)

    parser.add_argument('--ramp-up', help='Ramp-up time in seconds',
                        type=float, default=0.)

    parser.add_argument('--delay', help='Delay between each worker run',
                        type=float, default=0.)

    parser.add_argument('-p', '--processes', help='Number of processes',
                        type=int, default=1)

    parser.add_argument('-d', '--duration', help='Duration in seconds',
                        type=int, default=86400)

    parser.add_argument('-r', '--max-runs', help='Maximum runs per worker',
                        type=int, default=None)

    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='Quiet')

    parser.add_argument('-x', '--exception', action='store_true',
                        default=False,
                        help='Stop on first failure.')

    parser.add_argument('-c', '--console', action='store_true',
                        default=False,
                        help='Use simple console for feedback')

    parser.add_argument('--statsd', help='Activates statsd',
                        action='store_true', default=False)

    parser.add_argument('--statsd-server', help='Statsd Server',
                        type=str, default="127.0.0.1")

    parser.add_argument('--statsd-port', help='Statsd Port',
                        type=int, default=8125)

    parser.add_argument('--uvloop', help='Use uvloop', default=False,
                        action='store_true')
    return parser


def main():
    parser = _parser()
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.config:
        if args.scenario == 'loadtest.py':
            args.scenario = 'test'

        try:
            expand_options(args.config, args.scenario, args)
        except OptionError as e:
            print(str(e))
            sys.exit(0)

    if args.statsd:
        # early import to quit if no aiostatsd
        from aiostatsd.client import StatsdClient
        if StatsdClient is None:
            print('You need to install aiostatsd when using --statds')
            sys.exit(0)

    if args.uvloop:
        if PYPY:
            print("You can't use uvloop with PyPy")
            sys.exit(0)

        try:
            import uvloop
        except ImportError:
            print('You need to install uvloop when using --uvloop')
            sys.exit(0)

        import asyncio
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    return run(args)


def run(args):
    if not args.quiet:
        log('**** Molotov v%s. Happy breaking! ****' % __version__, pid=None)

    if os.path.exists(args.scenario):
        spec = spec_from_file_location("loadtest", args.scenario)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        try:
            import_module(args.scenario)
        except (ImportError, ValueError):
            print('Cannot import %r' % args.scenario)
            sys.exit(1)

    if len(get_scenarios()) == 0:
        print('You need at least one scenario. No scenario was found.')
        print('A scenario with a weight of 0 is ignored')
        sys.exit(1)

    if args.verbose > 0 and args.quiet:
        print("You can't use -q and -v at the same time")
        sys.exit(1)

    if args.verbose > 0 and not args.console:
        print("You have to be in console mode (-c) to use -v")
        sys.exit(1)

    if args.single_mode:
        if get_scenario(args.single_mode) is None:
            print("Can't find %r in registered scenarii" % args.single_mode)
            sys.exit(1)

    res = runner(args, screen=ui.init_screen)

    if not args.quiet:
        print('SUCCESSES: %(OK)d | FAILURES: %(FAILED)d\r' % res)
        print('*** Bye ***')
