#!/usr/bin/env python3
import asyncio


async def checked_call(cmd, *args) -> None:
    proc = await asyncio.create_subprocess_exec(cmd, *args)
    return_code = await proc.wait()
    if return_code != 0:
        raise ValueError(f"subprocess failed with exitcode {return_code}: {cmd} {args}")

async def start_fluidsynth():
    return checked_call(
            "/usr/bin/fluidsynth",
            "--audio-driver=alsa",
            "fluidsynth",
            "/usr/share/sounds/sf2/FluidR3_GM.sf2"
        )

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")


asyncio.run(run("ls /zzz"))
