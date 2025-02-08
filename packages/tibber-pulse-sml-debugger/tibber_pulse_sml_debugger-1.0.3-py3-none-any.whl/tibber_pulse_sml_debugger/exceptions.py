"""
A tiny application to see the data, that was recorded and send by your Tibber Pulse IR to your Tibber Pulse Bridge.

 Author: wh0ami
License: MIT License <https://opensource.org/license/MIT>
Project: https://codeberg.org/wh0ami/tibber-pulse-sml-debugger
"""


class AuthenticationError(Exception):
    """Authentication at the Tibber Pulse Bridge API failed."""
