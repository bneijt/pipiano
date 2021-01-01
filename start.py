#!/usr/bin/env python3
from typing import List, Tuple
import subprocess
import itertools

import logging
import sys
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def start(*cmd: str) -> subprocess.Popen:
    return subprocess.Popen(
        list(cmd),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def read_cmd_lines(*cmd: str) -> List[str]:
    p = start(*cmd)
    output_bytes, _ = p.communicate()
    p.wait()
    output = output_bytes.decode("utf-8")
    if p.returncode != 0:
        raise ValueError(
            f"Executing '{cmd}' failed and returned {p.returncode}:\n{output}"
        )
    return output.split("\n")


def fluidsynth():
    fluid_proc = subprocess.Popen(
        [
            "/usr/bin/fluidsynth",
            "--audio-driver=alsa",
            "--load-config",
            os.path.join(os.path.dirname(__file__), "fluid_config.txt"),
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    logger.info("Waiting for fluidsynth shell")
    for line in itertools.islice(fluid_proc.stdout, 30):
        if b"help topics" in line:
            break
    return fluid_proc


def select_client_num_from(lines: List[str], needle: str) -> str:
    """ Select the "client xxx" value from the first line containing needle"""
    try:
        return next(
            filter(lambda x: needle in x and x.startswith("client"), lines)
        ).split(":", 1)[0][len("client ") :]
    except StopIteration as stop_iteration:
        logger.error(f"Failed to find {needle} in {lines}")
        raise stop_iteration


def run() -> int:
    logger.info("Starting fluidsynth")
    fluidsynth_proc = fluidsynth()

    logger.info("aconnect-ing")
    input_client = select_client_num_from(
        read_cmd_lines("/usr/bin/aconnect", "--input"), "card=1"
    )

    output_client = select_client_num_from(
        read_cmd_lines("/usr/bin/aconnect", "--output"), "FLUID Synth"
    )
    logger.info(f"'{input_client}' -> '{output_client}'")
    try:
        read_cmd_lines("/usr/bin/aconnect", input_client, output_client)
    except ValueError as failure:
        if "Connection is already subscribed" not in str(failure):
            raise failure
    return fluidsynth_proc.wait()


def main():
    sys.exit(run())


if __name__ == "__main__":
    main()
