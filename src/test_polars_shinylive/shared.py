from pathlib import Path

import polars as pl

app_dir = Path(__file__).parent
df = pl.read_csv(app_dir / "penguins.csv")
