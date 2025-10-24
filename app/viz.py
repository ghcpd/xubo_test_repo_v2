from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd
import plotly.express as px

_DATE_COLUMN = "date"
_CATEGORY_COLUMN = "category"
_SALES_COLUMN = "sales"


def _ensure_datetime(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, errors="coerce")


def _ensure_numeric(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return series
    coerced = pd.to_numeric(series, errors="coerce")
    return coerced.fillna(0)


def load_data(path: Union[str, Path]) -> pd.DataFrame:
    file_path = Path(path).expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    df = pd.read_csv(file_path, parse_dates=[_DATE_COLUMN])
    df[_SALES_COLUMN] = _ensure_numeric(df[_SALES_COLUMN])
    df[_CATEGORY_COLUMN] = df[_CATEGORY_COLUMN].astype(str).str.strip()
    return df


def total_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working[_SALES_COLUMN] = _ensure_numeric(working[_SALES_COLUMN])
    if _CATEGORY_COLUMN not in working:
        working[_CATEGORY_COLUMN] = "Unknown"

    grouped = (
        working.groupby(_CATEGORY_COLUMN, dropna=False, sort=True)[_SALES_COLUMN]
        .sum()
        .reset_index()
        .sort_values(_SALES_COLUMN, ascending=False, kind="stable")
        .reset_index(drop=True)
    )
    return grouped


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()
    working[_DATE_COLUMN] = _ensure_datetime(working[_DATE_COLUMN])
    working[_SALES_COLUMN] = _ensure_numeric(working[_SALES_COLUMN])
    valid = working[_DATE_COLUMN].notna()
    if not valid.any():
        return pd.DataFrame({"month": pd.Series(dtype="object"), _SALES_COLUMN: pd.Series(dtype="float")})

    period_index = working.loc[valid, _DATE_COLUMN].dt.to_period("M")
    trend = (
        working.loc[valid]
        .groupby(period_index)[_SALES_COLUMN]
        .sum()
        .reset_index(name=_SALES_COLUMN)
    )
    trend["month"] = trend[_DATE_COLUMN].dt.strftime("%Y-%m")
    trend = trend.drop(columns=[_DATE_COLUMN]).sort_values("month").reset_index(drop=True)
    return trend[["month", _SALES_COLUMN]]


def generate_bar_chart(grouped_df: pd.DataFrame):
    fig = px.bar(
        grouped_df,
        x=_CATEGORY_COLUMN,
        y=_SALES_COLUMN,
        title="Sales by Category",
        labels={_CATEGORY_COLUMN: "Category", _SALES_COLUMN: "Sales (USD)"},
        hover_data={_CATEGORY_COLUMN: False, _SALES_COLUMN: ":.2f"},
        text_auto=".2s",
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Sales: %{y:,.2f}<extra></extra>",
        hoverlabel=dict(namelength=-1),
    )
    fig.update_layout(transition_duration=200)
    return fig


def generate_line_chart(trend_df: pd.DataFrame):
    sorted_trend = trend_df.sort_values("month")
    fig = px.line(
        sorted_trend,
        x="month",
        y=_SALES_COLUMN,
        title="Monthly Sales Trend",
        labels={"month": "Month", _SALES_COLUMN: "Sales (USD)"},
    )
    fig.update_traces(mode="lines+markers")
    return fig
