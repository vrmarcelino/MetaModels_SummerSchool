#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to read MICOM's grow workflow results and merge them in a single object

"""

# Load MICOM results from exported CSV files
# Folder structure:
#
# 2_Exchanges/
# ├── sample1_exchanges.csv
# ├── sample1_growth_rates.csv
# ├── sample2_exchanges.csv
# └── sample2_growth_rates.csv

from pathlib import Path
import pandas as pd
from types import SimpleNamespace


def load_micom_results(folder="2_Exchanges"):

    folder = Path(folder)

    exchange_files = sorted(folder.glob("*_exchanges.csv"))
    growth_files = sorted(folder.glob("*_growth_rates.csv"))
    annotation_files = sorted(folder.glob("*_annotations.csv"))

    if len(exchange_files) == 0:
        raise FileNotFoundError(
            f"No *_exchanges.csv files found in {folder}"
        )

    # ------------------------
    # Load exchanges
    # ------------------------

    exchange_tables = []

    for f in exchange_files:

        sample = f.name.replace("_exchanges.csv", "")

        df = pd.read_csv(f)

        df["sample_id"] = sample

        exchange_tables.append(df)

    exchanges = pd.concat(
        exchange_tables,
        ignore_index=True
    )

    # ------------------------
    # Load growth rates
    # ------------------------

    growth_rates = None

    if len(growth_files) > 0:

        growth_tables = []

        for f in growth_files:

            sample = f.name.replace(
                "_growth_rates.csv",
                ""
            )

            df = pd.read_csv(f)

            df["sample_id"] = sample

            growth_tables.append(df)

        growth_rates = pd.concat(
            growth_tables,
            ignore_index=True
        )

    # ------------------------
    # Load annotations
    # ------------------------

    annotations_tables = []

    for f in annotation_files:

        sample = f.name.replace("_annotations.csv", "")

        df = pd.read_csv(f)

        df["sample_id"] = sample

        annotations_tables.append(df)

    annotations = pd.concat(
        annotations_tables,
        ignore_index=True
    )



    # Create MICOM-like container

    res = SimpleNamespace(
        exchanges=exchanges,
        growth_rates=growth_rates,
        annotations = annotations_tables
    )

    return res

