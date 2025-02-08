#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File    : deloop
Author  : A. Dareau

Comments: a command line tool to deloop samples generated with the SP-404 looper
          (but could work with other kind of loopers)

          Usage :
              $> deloop fileA.wav fileB.wav output.wav
"""
# %% Imports
# std library
import sys
import wave
import array
import os
from pathlib import Path

# external dependencies
import typer
from typing_extensions import Annotated

# %% Help string

HELP_STRING = """
[DELOOP]

a command line tool to deloop samples generated with the SP-404 looper
(but could work with other kind of loopers)

Usage :
   $> deloop fileA.wav fileB.wav output.wav
"""


# %% Main


def delooper(
    file_a: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="🎵 The first wav file to unloop",
        ),
    ],
    file_b: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="🎵 The second wav file to unloop",
        ),
    ],
    file_out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            resolve_path=True,
            help="🎵 The path to the ouput file (defaults to /current_folder/out.wav)",
        ),
    ] = None,
):
    # -- PARSE INPUT
    if file_out is None:
        root = os.getcwd()
        file_out = Path(root) / "out.wav"
        if file_out.exists():
            msg = f"This will overwrite {file_out}, continue ?"
            overwrite = typer.confirm(msg)
            if not overwrite:
                print("Abort, Abort !!!!!")
                raise typer.Abort()
            print("Let's go !")

    # -- PROCESS
    # open first file
    with wave.open(str(file_a), "rb") as wave_file:
        params = wave_file.getparams()
        data_A = wave_file.readframes(wave_file.getnframes())

    # open second file
    with wave.open(str(file_b), "rb") as wave_file:
        data_B = wave_file.readframes(wave_file.getnframes())

    # convert bytes to numbers
    frames_A = array.array("h", data_A)
    frames_B = array.array("h", data_B)

    # sum
    sum_array = array.array("h")
    for sA, sB in zip(frames_A, frames_B):
        sum_array.append(sA - sB)

    # write out
    with wave.open(str(file_out), "wb") as wave_out:
        wave_out.setparams(params)
        wave_out.writeframes(sum_array.tobytes())

    # -- INFORM SUCCESS !!
    msg = f"""✨ 🌟 ✨ Sucess ✨ 🌟 ✨
🎵 Delooped file written in {file_out} 🎵"""
    print(msg)
