import polars as pl
from shiny.express import render, ui

ui.h2("Polars in Shinylive Test")


@render.ui
def version():
    return ui.pre(f"Polars version: {pl.__version__}")


@render.data_frame
def table():
    return pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
