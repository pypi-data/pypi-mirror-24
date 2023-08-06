import matplotlib.pyplot as plt
import seaborn as sns


def joyplot(data, x, row, row_order=None, palette=None,
            xlabel_suffix='log2(UMI + 1)', **kwargs):
    g = sns.FacetGrid(data, row=row, hue=row,
                      aspect=8, size=0.5, palette=palette,
                      row_order=row_order, **kwargs)
    # Draw the densities in a few steps
    g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
    g.map(sns.kdeplot, x, clip_on=False, color="w", lw=2, bw=.2)
    g.map(plt.axhline, y=0, lw=2, clip_on=False)

    # Define a function to add n=## to show the number of cells per cluster
    def show_size(x, color, label=None):
        ax = plt.gca()
        n = len(x)
        ax.text(1, 0.2, f'n={n}', color=color, ha='right', va='center',
                transform=ax.transAxes)

    g.map(show_size, x)

    # Define and use a simple function to label the plot in axes coordinates
    def label(x, color, label=None):
        if label is None:
            return
        ax = plt.gca()
        ax.text(0, .2, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    g.map(label, x)

    g.set_xlabels(f'{x} {xlabel_suffix}')

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25)

    # Remove axes details that don't play will with overlap
    g.set_titles("")
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    
    return g