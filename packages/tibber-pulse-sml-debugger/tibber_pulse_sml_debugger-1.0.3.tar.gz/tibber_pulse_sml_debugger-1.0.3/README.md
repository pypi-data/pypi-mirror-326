# The ultimate Tibber Pulse SML Debugging tool

This is a tiny Python-based CLI app, that helps you to dig a little bit deeper
into the communication of your electric meter and your Tibber Pulse.

You know it: The data from your electric meter doesn't show up in your Tibber
app, the Tibber app tells you to rotate the Pulse IR for the 168546854468498th
time for a little bit, the usage data in your Tibber app updates only once per
hour or whatever.

You don't really know, when the Tibber Pulse IR is at the correct position, and
you also don't know whether your electric meter is doing weird stuff or so.

This app may help you. It polls the data from the local web server of the Tibber
Pulse Bridge in a short interval and directly shows you, what happens, if you
turn the head of your Pulse IR a little bit.

This project is not affiliated to Tibber. I am just a normal Tibber customer
and I also don't get any money, discounts or whatever for this. This app is
thought as a "customers help customers"-project.

## Usage

### Installation

This project is published on
[PyPI](https://pypi.org/project/tibber-pulse-sml-debugger/), so you just want
to install it via pipx or pip. Please note, that pipx is the recommended way.

```commandline
$ pipx install tibber-pulse-sml-debugger
 
OR

$ pip install tibber-pulse-sml-debugger
```

### Activating the web server in the Tibber Pulse Bridge

Please note, that you MUST activate the local webserver of your Tibber Pulse
Bridge. I will provide a tutorial here, but cannot assume any warranties or
liabilities, whether this is working or turning your Tibber Pulse into a
singing toaster or something...

1. Remember/Write down the password of your Tibber Pulse. It can be found on the
   bottom side of the Bridge.
2. Bring your Bridge in AP mode - citation from my manual: "[...] unplug the
   device from your socket and plug it in again 2 times. After the first time,
   you plug it in, the LED will light up red, then white, then yellow. Once
   you've plugged it in for the second time, the LED will light up red, then
   white, then green [...]"
3. Connect to the WiFi network of the Bridge - use the password from step 1
4. Open [http://10.133.70.1](http://10.133.70.1) in your browser and log in
   with **admin** and the password from step 1.
5. Go to the tab console and execute the following commands:
   1. `param_set 39 TRUE`
   2. `param_store`
6. Wait ~1 minute.
7. Remove the Bridge from your socket, wait a few seconds and plug it back in
8. (Optional) If not already known, find out the IP address of your Tibber
   Pulse Bridge via e.g. your routers web interface.
9. You can now access the web server of your bridge in your WiFi network.

### Use the app

After the installation, the app can be executed via the command
`tibber-pulse-sml-debugger` or just `tpsd`.

So if you just want to see, whether your Tibber Pulse is reporting valid data,
just execute it like this:

```commandline
$ tpsd --address 192.0.2.123 --password PASS-WORD
2024-11-20 20:13:10.868 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
2024-11-20 20:13:11.997 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
2024-11-20 20:13:13.027 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
^C2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:133 - +++ STATISTICS +++
2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:137 - Total responses: 3
2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:138 - Valid responses: 3 (100.0%)
2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:139 - Empty responses: 0 (0.0%)
2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:142 - CrcError responses: 0 (0.0%)
2024-11-20 20:13:13.241 | INFO     | tibber_pulse_sml_debugger.main:main:145 - Responses with other errors: 0 (0.0%)
```

If you want to see, what's reported by your electric meter in detail, you want
to pass `--debug`:

```commandline
$ tpsd --address 192.0.2.123 --password PASS-WORD --debug
2024-11-20 20:14:22.039 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
2024-11-20 20:14:22.040 | DEBUG    | tibber_pulse_sml_debugger.main:main:105 - +++ SML DATA +++
2024-11-20 20:14:22.040 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Bezug Total -> 123456789.4 Wh
2024-11-20 20:14:22.040 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Einspeisung Total -> 123456.4 Wh
2024-11-20 20:14:22.040 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - aktuelle Wirkleistung -> 414 W
2024-11-20 20:14:23.096 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
2024-11-20 20:14:23.096 | DEBUG    | tibber_pulse_sml_debugger.main:main:105 - +++ SML DATA +++
2024-11-20 20:14:23.096 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Bezug Total -> 123456789.6 Wh
2024-11-20 20:14:23.096 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Einspeisung Total -> 123456.4 Wh
2024-11-20 20:14:23.096 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - aktuelle Wirkleistung -> 413 W
2024-11-20 20:14:24.186 | INFO     | tibber_pulse_sml_debugger.main:main:104 - Valid SML data received!
2024-11-20 20:14:24.186 | DEBUG    | tibber_pulse_sml_debugger.main:main:105 - +++ SML DATA +++
2024-11-20 20:14:24.186 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Bezug Total -> 123456789.7 Wh
2024-11-20 20:14:24.186 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - Zählerstand Einspeisung Total -> 123456.4 Wh
2024-11-20 20:14:24.186 | DEBUG    | tibber_pulse_sml_debugger.main:main:107 - aktuelle Wirkleistung -> 413 W
^C2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:133 - +++ STATISTICS +++
2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:137 - Total responses: 3
2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:138 - Valid responses: 3 (100.0%)
2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:139 - Empty responses: 0 (0.0%)
2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:142 - CrcError responses: 0 (0.0%)
2024-11-20 20:14:24.492 | INFO     | tibber_pulse_sml_debugger.main:main:145 - Responses with other errors: 0 (0.0%)
```

All command line options are also listed and described below:

| Option             | Effect                                                                                                                                                           |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h`, `--help`     | Shows a help message and exit.                                                                                                                                   |
| `-u`, `--username` | The username of your Tibber Pulse Bridge web server. Defaults to the factory default 'admin'.                                                                    |
| `-p`, `--password` | The password of your Tibber Pulse Bridge web server.                                                                                                             |
| `-n`, `--node-id`  | The Node ID of your Tibber Pulse IR. Defaults to 1, which is not correct some times. You will find the Node ID in the web interface of your Tibber Pulse Bridge. |
| `-i`, `--interval` | The interval for polling the API of your Tibber Pulse Bridge. Defaults to one second.                                                                            |
| `-d`, `--debug`    | Whether all meter data should be logged to stdout.                                                                                                               |

## Update

You can update via pipx/pip by using the following commands:

```commandline
$ pipx upgrade tibber-pulse-sml-debugger
 
OR

$ pip install --upgrade tibber-pulse-sml-debugger
```

## Development

This is a uv project. You can set up your development environment by cloning
this Repository via `git` and running a `uv sync` in the project
directory afterward.

The Lockfile can be updated by using `uv lock` (also updates the installed
packages in the dependency tree).

The project can be bundled by running `uv build` and published by running
`uv publish`. Results can be found in the `dist/` directory.

For code linting and formatting, `ruff` was used. You may run it via `uv run ruff check` or `uv run ruff format`.

## Tests

The app was manually tested with Python 3.10 on Ubuntu 22.04, but _should_ also
run with any newer Python3 version and every other OS, that is supported by
Python3.

It was tested with the following electric meters, but should work with all
electric meters, that are sending valid SML data (feel free to contribute):

- Landis+Gyr E320
- Landis+Gyr E220

## Tips, if you are facing many CrcErrors

- Clean the head of your Pulse IR and the IR interface on your electric meter.
  Display cleaner and a clean microfiber cloth worked quite good in my case.
- If you can, remove the head from the Pulse IR and DO NOT place the complete
  Pulse IR onto your electric meter. Just place the head onto it and lay the
  Pulse IR e.g. on top of the electric meter. The Pulse IR is too heavy to stay
  reliable at the same position, and you need to place it again, if you want to
  replace the batteries in it.
- The 6 o'Clock position, which is recommended by Tibber at the beginning,
  doesn't really work with the mentioned Landis+Gyr electric meters above.
  Its "working", but 99% of the messages are CrcErrors. I found the correct
  position between 5 and 6 o'Clock, closer to 5 o'Clock.
- Turn the head of the Pulse IR very slowly and only step by step / millimeter
  by millimeter and wait a little bit for the output of this app.
  Normally, there should be almost no messages with CRC errors.
- There's a bug with the Pulse IR and at least Landis+Gyr meters, where all
  30-45 seconds, there are only empty SML frames for 10+-5 seconds.

## Special Thanks

- To my friend David, who motivated me to publish this project, after we
  successfully debugged his (and also mine) Pulse/Meter by using this project.
- To Jetbrains for the free IDE PyCharm, that was used for this project.
- To all maintainers of the dependencies of this project.

## Contribution

You are welcome to contribute to this project. Also field reports are welcome!
