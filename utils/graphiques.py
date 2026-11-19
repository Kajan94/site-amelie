import base64
from io import BytesIO
from textwrap import fill

import matplotlib.ticker as ticker
from matplotlib.figure import Figure

import model.db as db


def graphique(annee=None):
    """Histogramme vertical des montants moyens nationaux par poste."""
    data = db.montant_moyen_prescriptions(annee)
    if data.empty:
        return None

    figure = Figure(figsize=(8, 6), facecolor="#f1f6ff", layout="constrained")
    ax = figure.subplots()
    labels = [fill(label, width=22) for label in data["libelle_poste_prescription"]]
    ax.bar(labels, data["montant_moyen"],
           color="black", edgecolor="black")
    ax.set_xlabel("Poste de prescription")
    ax.set_ylabel("Montant moyen des prescriptions (en milliers d’€)")
    ax.tick_params(axis="x", labelrotation=20)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.5, color="gray")
    ax.set_facecolor("#f1f6ff")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda value, _: f"{value / 1_000:,.0f}".replace(",", " ")
    ))
    selected_year = annee if annee is not None else int(data["Annee"].iloc[0])
    ax.set_title(f"Montant moyen des prescriptions en France en {selected_year}")
    return image_png(figure)


def graphique_camembert_prescriptions(annee=None):
    """Deux anneaux : régions métropolitaines et régions d’outre-mer."""
    data = db.comparaison_prescriptions_par_region(annee)
    if data.empty:
        return None

    # Le total national est exclu dans la requête SQL. Conserver ici
    # l’Île-de-France et les Hauts-de-France, qui sont bien des régions.
    overseas = data["region"].isin([
        "Guadeloupe", "Martinique", "Guyane", "La Réunion", "La Reunion", "Mayotte"
    ])
    groups = (data[~overseas], data[overseas])
    figure = Figure(figsize=(12, 8), facecolor="#f1f6ff", layout="constrained")
    axes = figure.subplots(1, 2)
    colors = ["#D5FFB4", "#B7FF81", "#D0E4FF", "#AED1FF", "#87af6b"]

    for ax, group, title in zip(axes, groups, ("France métropolitaine", "Outre-mer")):
        ax.set_title(title)
        values = group["prescriptions_totales"]
        if group.empty or values.sum() <= 0:
            ax.text(0.5, 0.5, "Aucune donnée publiée", ha="center", va="center",
                    transform=ax.transAxes)
            ax.set_axis_off()
            continue
        ax.pie(
            values,
            labels=group["region"].replace("Ile-de-France", "Île-de-France"),
            autopct="%1.1f%%",
            explode=[0.1 if title == "France métropolitaine" else 0] * len(group),
            startangle=140,
            colors=(colors * (len(group) // len(colors) + 1))[:len(group)],
            textprops={"fontsize": 10, "color": "black"},
            wedgeprops={"width": 0.4},
        )
    return image_png(figure)


def image_png(figure):
    with BytesIO() as image:
        figure.savefig(image, format="png", bbox_inches="tight", facecolor=figure.get_facecolor())
        return "data:image/png;base64," + base64.b64encode(image.getvalue()).decode("ascii")
