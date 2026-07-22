"""
Trading signal generation utilities for pairs trading.
"""

from __future__ import annotations

import pandas as pd



def generate_signals(
    zscore: pd.Series,
    entry_threshold: float = 2.0,
    exit_threshold: float = 0.0
) -> pd.DataFrame:
    """
    Generate pairs trading signals based on z-score.

    Rules:

    Z-score < -entry_threshold:
        Long spread

    Z-score > entry_threshold:
        Short spread

    Z-score near zero:
        Exit position

    Parameters
    ----------
    zscore : pd.Series

    entry_threshold : float

    exit_threshold : float

    Returns
    -------
    pd.DataFrame
    """

    signals = pd.DataFrame(
        index=zscore.index
    )

    signals["Zscore"] = zscore


    signals["Position"] = 0


    # Long spread
    signals.loc[
        zscore < -entry_threshold,
        "Position"
    ] = 1


    # Short spread
    signals.loc[
        zscore > entry_threshold,
        "Position"
    ] = -1


    # Exit
    signals.loc[
        abs(zscore) <= exit_threshold,
        "Position"
    ] = 0


    return signals



def calculate_position_changes(
    signals: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate trading events.

    Parameters
    ----------
    signals : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    signals = signals.copy()


    signals["Trade"] = (
        signals["Position"]
        .diff()
    )


    return signals