"""
A tiny application to see the data, that was recorded and send by your Tibber Pulse IR to your Tibber Pulse Bridge.

 Author: wh0ami
License: MIT License <https://opensource.org/license/MIT>
Project: https://codeberg.org/wh0ami/tibber-pulse-sml-debugger
"""

import sys
import traceback
from time import sleep

import requests
from loguru import logger
from smllib.errors import CrcError

from tibber_pulse_sml_debugger.exceptions import AuthenticationError
from tibber_pulse_sml_debugger.helper import display_final_report, fetch_data, setup_parser


def main() -> None:
    """argparse, logger setup, etc."""
    # initialize cli argument parser
    args = setup_parser()

    # configure the logger
    logger.remove()
    logger.add(sys.stdout, level="DEBUG" if args.debug else "INFO")

    # initialize requests for authentication against the bridge
    session = requests.Session()
    session.auth = (args.username, args.password)

    # initialize all counters
    responses_total = 0
    responses_with_crc_errors = 0
    responses_with_empty_sml_frames = 0
    responses_with_other_errors = 0
    exit_code = 0

    # run the actual application logic
    try:
        while True:
            try:
                responses_total += 1
                response = fetch_data(
                    session=session,
                    node_id=args.node_id,
                    address=args.address,
                )
                logger.info("Valid SML data received!")
                logger.debug("+++ SML DATA +++")
                for result in response:
                    logger.debug(result)
            except AttributeError:
                responses_with_empty_sml_frames += 1
                logger.error("Bytes missing / SML frame is empty object!")
            except CrcError:
                responses_with_crc_errors += 1
                logger.error("Data invalid / CrcError while validating the SML frame!")
            except Exception:
                responses_with_other_errors += 1
                raise
            finally:
                sleep(args.interval)
    except KeyboardInterrupt:
        pass
    except requests.exceptions.ConnectionError:
        logger.error(
            "Timeout while connecting to your Tibber Pulse Bridge. Have you activated the web server in your Tibber "
            "Pulse Bridge?",
        )
        exit_code = 1
    except AuthenticationError:
        logger.error("Passed username or password was rejected by your Tibber Pulse Bridge!")
        exit_code = 2
    except Exception:  # noqa: BLE001
        logger.error(traceback.format_exc())
        exit_code = 3
    finally:
        display_final_report(
            responses_total=responses_total,
            responses_with_empty_sml_frames=responses_with_empty_sml_frames,
            responses_with_crc_errors=responses_with_crc_errors,
            responses_with_other_errors=responses_with_other_errors,
        )
        sys.exit(exit_code)


# run the main class
if __name__ == "__main__":
    main()
