import matplotlib.pyplot as plt
from pathlib import Path



# ============================================================
# FORECAST PLOT
# ============================================================

def plot_forecast(
    y_true,
    y_pred,
    country,
    model_name,
    output_dir
):


    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    plt.figure(
        figsize=(14,5)
    )


    plt.plot(
        y_true.index,
        y_true.values,
        label="Actual"
    )


    plt.plot(
        y_pred.index,
        y_pred.values,
        label="Forecast"
    )


    plt.title(
        f"{country.upper()} - {model_name}"
    )


    plt.xlabel(
        "Time"
    )


    plt.ylabel(
        "Price EUR/MWh"
    )


    plt.legend()


    plt.grid(
        True
    )


    file_name = (
        f"{country}_{model_name}.png"
        .replace(
            " ",
            "_"
        )
    )


    plt.savefig(
        output_dir / file_name,
        bbox_inches="tight"
    )


    plt.close()