import plotly.express as px
import polars as pl
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget

from .shared import app_dir, df

ui.page_opts(
    title="Penguins dashboard",
    fillable=True,
)


with ui.sidebar(title="Filter controls"):
    ui.input_dark_mode(id="mode")
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render_widget
        def length_depth():
            template = (
                "plotly_dark" if input.mode() == "dark" else "plotly_white"
            )
            fig = px.scatter(
                filtered_df().to_pandas(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
                template=template,
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            return fig

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df() -> pl.DataFrame:
    return df.filter(
        pl.col("species").is_in(input.species()),
        pl.col("body_mass_g") < input.mass(),
    )
