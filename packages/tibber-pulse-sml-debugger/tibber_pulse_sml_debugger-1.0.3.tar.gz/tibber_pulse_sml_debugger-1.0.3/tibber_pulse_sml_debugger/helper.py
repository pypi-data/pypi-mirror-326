"""
A tiny application to see the data, that was recorded and send by your Tibber Pulse IR to your Tibber Pulse Bridge.

 Author: wh0ami
License: MIT License <https://opensource.org/license/MIT>
Project: https://codeberg.org/wh0ami/tibber-pulse-sml-debugger
"""

import argparse
import sys

import requests
import smllib.sml.response_get_list
from loguru import logger
from smllib import SmlStreamReader, const

from tibber_pulse_sml_debugger.exceptions import AuthenticationError


def percentage(total: int, part: int) -> str:
    """
    Calculate and format the percentage of two integers.

    :param total: The total amount for the percentage calculation.
    :param part: The part amount for the percentage calculation.
    :return: The percentage of the part value from the total value as a string, followed by the % symbol.
    """
    percentage_value = round((part / (total / 100)), 2)
    return f"{percentage_value}%"


def fetch_data(session: requests.Session, address: str, node_id: int) -> list[str]:
    """
    Fetch and process the SML data from a Tibber Pulse Bridge web server.

    :param session: The requests session with the auth data.
    :param address: The hostname or IP address of the Tibber Pulse Bridge web server.
    :param node_id: The node ID of the Tibber Pulse IR.
    """
    raw_sml_data = session.get(f"http://{address}/data.json?node_id={node_id}", timeout=10)
    if raw_sml_data.status_code == 401:
        raise AuthenticationError

    sml_stream = SmlStreamReader()
    sml_stream.add(raw_sml_data.content)

    sml_frame = sml_stream.get_frame()

    results = []

    parsed_sml_messages = sml_frame.parse_frame()
    for message in parsed_sml_messages:
        if isinstance(message.message_body, smllib.sml.response_get_list.SmlGetListResponse):
            for list_entry in message.message_body.val_list:
                if list_entry.obis in const.OBIS_NAMES:
                    obis_name = const.OBIS_NAMES[list_entry.obis]
                else:
                    continue
                obis_unit = const.UNITS[list_entry.unit] if list_entry.unit and list_entry.unit in const.UNITS else ""
                results.append(f"{obis_name} -> {list_entry.get_value()} {obis_unit}")
    return results


def display_final_report(
    responses_total: int,
    responses_with_empty_sml_frames: int,
    responses_with_crc_errors: int,
    responses_with_other_errors: int,
) -> None:
    """Show the final report at the end of the script."""
    logger.info("+++ STATISTICS +++")
    responses_valid = (
        (responses_total - responses_with_empty_sml_frames) - responses_with_crc_errors
    ) - responses_with_other_errors
    logger.info(f"Total responses: {responses_total}")
    logger.info(f"Valid responses: {responses_valid} ({percentage(responses_total, responses_valid)})")
    logger.info(
        f"Empty responses: {responses_with_empty_sml_frames} "
        f"({percentage(responses_total, responses_with_empty_sml_frames)})",
    )
    logger.info(
        f"CrcError responses: {responses_with_crc_errors} ({percentage(responses_total, responses_with_crc_errors)})",
    )
    logger.info(
        f"Responses with other errors: {responses_with_other_errors} "
        f"({percentage(responses_total, responses_with_other_errors)})",
    )


def setup_parser() -> argparse.Namespace:
    """Create a command line parser."""
    parser = argparse.ArgumentParser(
        description="A tiny python based CLI application to see the data, that was recorded and send by your Tibber "
        "Pulse IR to your Tibber Pulse Bridge.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # read cli parameters
    parser.add_argument(
        "-a",
        "--address",
        metavar="<hostname or IP address>",
        type=str,
        required=True,
        help="The hostname or IP address of your Tibber Pulse Bridge. Please note, that the local webserver must be "
        "activated.",
    )
    parser.add_argument(
        "-u",
        "--username",
        metavar="<username>",
        type=str,
        default="admin",
        required=False,
        help="The username of your Tibber Pulse Bridge web server. Defaults to the factory default 'admin'.",
    )
    parser.add_argument(
        "-p",
        "--password",
        metavar="<password>",
        type=str,
        required=True,
        help="The password of your Tibber Pulse Bridge web server.",
    )
    parser.add_argument(
        "-n",
        "--node-id",
        metavar="<Pulse IR node ID>",
        type=int,
        default=1,
        required=False,
        help="The Node ID of your Tibber Pulse IR. Defaults to 1, which is not correct some times. You will find the "
        "Node ID in the web interface of your Tibber Pulse Bridge.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        metavar="<amount of seconds>",
        type=int,
        default=1,
        required=False,
        help="The interval for polling the API of your Tibber Pulse Bridge. Defaults to one second.",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Whether all meter data should be logged to stdout.",
    )

    # actually parse the arguments that were passed
    return parser.parse_args(sys.argv[1:])
