"""Command-line interface for LiquidSig cfRNA deconvolution.

This module provides a command-line interface for analyzing cell-free RNA (cfRNA)
data using tissue and cell-type marker genes from the CZI CellGuide database.
"""

import os
import time
from importlib.metadata import version

import click
import pandas as pd
import requests
import pyranges

from liquidsig.deconvolution import HierarchicalDeconvolution


def flatten_series(series: pd.Series) -> pd.DataFrame:
    """Flatten nested CZI CellGuide API data into a DataFrame.

    Args:
        series: Series containing nested dictionaries of tissue/cell marker data
               Format: {tissue: {cell_type_id: [{marker data}]}}

    Returns:
        DataFrame with (hopefully) columns:
        - tissue: Tissue name
        - cell_type_id: Cell type identifier
        - marker_score: Effect size of marker gene
        - me: Mean expression (ln(cppt+1) normalized)
        - pc: Percentage of cells expressing gene
        - gene: Gene name
    """
    data = []
    for tissue, cell_types in series.items():
        for cell_type_id, markers in cell_types.items():
            for marker in markers:
                row = {"tissue": tissue, "cell_type_id": cell_type_id}
                row.update(marker)
                data.append(row)
    return pd.DataFrame(data)


def get_references(reference_dir: str = "references") -> tuple[str, str]:
    """Download and cache reference data for LiquidSig.

    Args:
        reference_dir: Directory to store reference data (default: 'references')

    Returns:
        Tuple containing:
        - gencode_gtf_file: Path to GENCODE GTF file
        - marker_file: Path to marker gene data file
    """

    # Let's download the marker data from CZBioHub's CellGuide
    # Per discussion with Max Lombardo on Slack, this is a snapshot from Q2/Q3 2024
    # We can also scrape the individual json files, but it's tedious -- hopefully their API allows a clearer access later.

    # Download this URL and save it into a references/ directory, only if it doesn't already exist:
    marker_data_url = "https://cellguide.cellxgene.cziscience.com/1716401368/computational_marker_genes/marker_gene_data.json.gz"
    marker_file = os.path.join(reference_dir, "marker_gene_data.json.gz")

    if not os.path.exists(reference_dir):
        os.makedirs(reference_dir)

    if not os.path.exists(marker_file):
        click.echo(f"Downloading marker data from {marker_data_url}")
        response = requests.get(marker_data_url, timeout=30)
        response.raise_for_status()
        with open(marker_file, "wb") as f:
            f.write(response.content)
    else:
        click.echo(f"\nMarker data cache exists at: {marker_file}")

    # Also download the Gencode .GTF for annotations / transcript data
    # Note this is the *FULL* GENCODE GTF that includes scaffolds like "ENSG00000275405"
    # We probably also need to download the lncRNA variant version?
    gencode_gtf_url = "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_47/gencode.v47.chr_patch_hapl_scaff.annotation.gtf.gz"
    gencode_gtf_file = os.path.join(
        reference_dir, "gencode.v47.chr_patch_hapl_scaff.annotation.gtf.gz"
    )

    if not os.path.exists(gencode_gtf_file):
        click.echo(f"Downloading GENCODE GTF data from {gencode_gtf_url}")
        response = requests.get(gencode_gtf_url, timeout=30)
        response.raise_for_status()
        with open(gencode_gtf_file, "wb") as f:
            f.write(response.content)
    else:
        click.echo(f"GENCODE GTF cache exists at {gencode_gtf_file}\n")

    return gencode_gtf_file, marker_file


def load_transcript_quants(
    transcript_quants: str, verbose: bool = False
) -> pd.DataFrame:
    """Load transcript quantification data from a file.

    Args:
        transcript_quants: Path to transcript quantification file (e.g., Salmon quant.sf)
        verbose: Enable verbose output

    Returns:
        DataFrame containing transcript quantification data
    """
    click.echo("Loading transcript quants.")
    transcript_quants_df = pd.read_csv(transcript_quants, sep="\t")

    # Assert that the transcript quants file has the expected columns
    if verbose:
        click.echo("Validating transcript quants columns.\n")
    expected_columns = ["Name", "Length", "EffectiveLength", "TPM", "NumReads"]
    assert all(
        column in transcript_quants_df.columns for column in expected_columns
    ), f"Expected columns: {expected_columns}"

    if verbose:
        click.echo(transcript_quants_df.head())

    return transcript_quants_df


def load_marker_data(
    marker_file: str, organism: str, verbose: bool = False
) -> tuple[pd.DataFrame, list[str]]:
    """Load marker gene data from a file.

    Args:
        marker_file: Path to marker gene data file
        organism: Organism to analyze
        verbose: Enable verbose output

    Returns:
        Tuple containing:
        - DataFrame containing marker gene data
        - List of distinct marker genes
    """
    if organism != "Homo sapiens":
        click.secho("Warning: NOT tested on non-human data yet.", fg="red", bold=True)

    click.echo("Loading marker data.")

    marker_data = pd.read_json(marker_file, compression="gzip")
    if verbose:
        click.echo("\nMarker data:")
        click.echo(marker_data.head())
        click.echo("\nObserved organisms: " + ",".join(marker_data.columns.to_list()))

    # filtered_marker_data is a dataframe of tissues & cell types w/ corresponding markers
    #  Explained a bit in: https://cellxgene.cziscience.com/docs/04__Analyze%20Public%20Data/4_2__Gene%20Expression%20Documentation/4_2_5__Find%20Marker%20Genes ?
    # e.g. filtered_marker_data['heart']['CL:4033054']
    #    [{'marker_score': 1.6855389931276041,   # AKA effect size. Indicates how much higher the average gene expression is in this cell type relative to other cell types in the same tissue.
    #     'me': 3.168754253595605, # Mean expression average(ln(cppt+1))-normalized gene expression among cells in the cell type
    #     'pc': 0.821720388599369,  # Percentage of cells expressing a gene in the cell type (?)
    #     'gene': 'PLA2G5'}

    # Note some have tissue entries but nan data (e.g., "urethra" and "urinary bladder")
    # TODO: Sort out ontology to better manage these? e.g. there's a "bladder organ" which has markers, but not "urinary bladder"
    filtered_marker_data = marker_data[organism].dropna()
    filtered_marker_data = filtered_marker_data.drop("All Tissues")

    assert (
        len(filtered_marker_data.index) > 0
    ), f"No tissues with marker genes found for {organism}."

    if verbose:
        click.echo(f"Tissues found: {len(filtered_marker_data.index)}")
        click.echo("\t" + ",".join(filtered_marker_data.index.to_list()))

    # Flatten the nested marker data into a DataFrame
    flattened_filtered_marker_data = flatten_series(filtered_marker_data)

    # TODO: Just drop this return and have downstream stuff call the dataframe directly.
    # See how many distinct genes are in the column 'gene' in flattened_filtered_marker_data
    # This is the list of marker genes we'll use for deconvolution
    distinct_cellgene_markers: list[str] = (
        flattened_filtered_marker_data["gene"].dropna().unique().tolist()  # type: ignore
    )

    # Some CZI entries lack genes -- Likely the CZI snapshot has some errors, or it's an ontology issue.
    malformed_entry_count = flattened_filtered_marker_data["gene"].isnull().sum()

    if verbose:
        click.echo(
            f"\nMalformed entries (no gene) in CellGene markers: {malformed_entry_count}"
        )
        click.echo(
            f"\n{len(distinct_cellgene_markers)} distinct marker genes found in {organism}."
        )

    # TODO: Hackish -- must fix this later
    renamed_flattened_filtered_marker_data = flattened_filtered_marker_data.rename(
        columns={
            "tissue": "Tissue",
            "cell_type_id": "Cell",
            "marker_score": "GeneMarkerScore",
            "me": "GeneMeanExpression",
            "pc": "GenePercentExpressing",
            "gene": "GeneName",
        }
    )

    return renamed_flattened_filtered_marker_data, distinct_cellgene_markers


def load_gencode_gtf(gencode_gtf_file: str, verbose: bool = False) -> pd.DataFrame:
    """Load GENCODE GTF data from a file.

    Args:
        gencode_gtf_file: Path to GENCODE GTF file
        verbose: Enable verbose output

    Returns:
        DataFrame containing GENCODE GTF data
    """
    click.echo("Loading GENCODE GTF data.")
    gencode_df = pyranges.read_gtf(gencode_gtf_file, as_df=True)

    # Filter the GTF to only include gene entries
    # TODO: explore lncRNAs - lots of data there
    gencode_genes_df = gencode_df[gencode_df.Feature == "gene"]

    # The gencode gene_id is suffixed by the ensembl version (e.g. ENSG00000237491.11) -- so we drop the period and any characters after it
    gencode_genes_df.loc[:, "gene_id"] = (
        gencode_genes_df["gene_id"].str.split(".").str[0]
    )

    if verbose:
        click.echo(gencode_genes_df.head())

    return gencode_genes_df


def coalesce_transcripts(transcript_quants_df: pd.DataFrame) -> pd.DataFrame:
    """Coalesce transcript-level data into gene-level data.

    Args:
        transcript_quants_df: DataFrame containing transcript quantification data

    Returns:
        DataFrame containing gene-level quantification data

    Raises:
        NotImplementedError: Transcript-level quantification not yet supported
    """
    # Find transcripts of the same gene and compute a new TPM
    # Note we cannot simply sum the TPMs, as the effective length of the gene is different

    if "ENST" in transcript_quants_df["Name"].iloc[0]:
        raise NotImplementedError("Transcript-level quantification not yet supported.")
    return transcript_quants_df


def harmonize_gene_names(
    transcript_quants_df: pd.DataFrame, gencode_df: pd.DataFrame, verbose: bool = False
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Harmonize gene names between transcript quants and GENCODE GTF data.

    NOTE: This will also coalesce individual transcripts into genes.

    Args:
        transcript_quants_df: DataFrame containing transcript quantification data
        gencode_df: DataFrame containing GENCODE GTF data
        verbose: Enable verbose output

    Returns:
        Tuple containing:
        - DataFrame containing harmonized gene-level quantification data
        - DataFrame containing unannotated genes
    """

    # See if our quant has ENSG or gene names
    first_quant_entry = transcript_quants_df["Name"].iloc[0]

    if verbose:
        click.echo(
            f"Processing gene names in quant file using first entry: {first_quant_entry}"
        )

    if first_quant_entry.startswith("ENST"):
        click.echo(
            "Transcript-level quantification detected, converting to gene-level."
        )
        transcript_quants_df = coalesce_transcripts(transcript_quants_df)

    total_gene_count = len(transcript_quants_df)
    unique_gene_count = len(set(transcript_quants_df["Name"].values))

    click.echo(f"Total genes in your quant: {total_gene_count}")
    click.echo(f"Unique genes in your quant: {unique_gene_count}")
    if total_gene_count != unique_gene_count:
        click.secho(
            f"\tWarning: {total_gene_count - unique_gene_count} duplicate genes in your quant.",
            fg="yellow",
            bold=True,
        )
        click.echo(
            "This is strange. Why are there duplicates? Double-check your input data."
        )
    click.echo("")

    # Store unannotated genes in a separate dataframe
    unannotated_quants_df = pd.DataFrame()

    if first_quant_entry.startswith("ENSG"):
        click.echo("ENSG prefix detected, converting to common gene name.")
        # We want to convert the column transcript_quants_df['Name'] to gene names, using the gencode_genes dataframe.
        # Specifically, we want to use gencode_genes["gene_name"] where gencode_genes["gene_id"] == transcript_quants_df["Name"]
        polished_quants_df = transcript_quants_df.merge(
            gencode_df, left_on="Name", right_on="gene_id", how="inner"
        )
        click.echo(
            f"*Distinct* genes by GENCODE name: {len(set(polished_quants_df['gene_name'].values))}"
        )

        # Also calculate the number of genes that are not in the GTF
        missing_genes = set(transcript_quants_df["Name"].values) - set(
            gencode_df["gene_id"].values
        )

        unannotated_quants_df = transcript_quants_df[
            transcript_quants_df["Name"].isin(missing_genes)
        ]

    else:
        # If this is incorrect, please file a bug at github.com/semenko/liquidsig
        click.echo(
            "No ENST or ENSG prefix, assuming ENSEMBL/GENCODE gene names are already present."
        )
        polished_quants_df = transcript_quants_df

    return polished_quants_df, unannotated_quants_df


def export_tissue_figures(run_results_path, tissue_figures) -> None:
    """
    Export figures to output directory.

    Args:
        run_results_path: Path to output directory
        tissue_figures: Dictionary of tissue figures
    """
    # To display figures:
    # plt.show() # This will display all generated figures

    # # To save figures (optional):
    tissue_figures["proportion"].savefig(
        os.path.join(run_results_path, "tissue_proportions.png")
    )
    tissue_figures["scatter"].savefig(
        os.path.join(run_results_path, "tissue_scatter.png")
    )
    tissue_figures["marker_heatmap"].savefig(
        os.path.join(run_results_path, "tissue_marker_heatmap.png")
    )
    tissue_figures["residual"].savefig(
        os.path.join(run_results_path, "tissue_residual_plot.png")
    )


def export_cell_figures(
    cell_results_path,
    cell_proportion_figures_dict,
    cell_scatter_figures_dict,
    cell_marker_heatmap_figures_dict,
    cell_residual_figures_dict,
) -> None:
    """
    Export cell figures to output directory.

    Args:
        cell_results_path: Path to cell output directory
        cell_proportion_figures_dict: Dictionary of cell proportion figures
        cell_scatter_figures_dict: Dictionary of cell scatter figures
        cell_marker_heatmap_figures_dict: Dictionary of cell marker heatmap figures
        cell_residual_figures_dict: Dictionary of cell residual figures
    """

    for tissue, fig in cell_proportion_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(cell_results_path, f"cell_proportions_{tissue}.png")
            )
    for tissue, fig in cell_scatter_figures_dict.items():
        if fig:
            fig.savefig(os.path.join(cell_results_path, f"cell_scatter_{tissue}.png"))

    for tissue, fig in cell_marker_heatmap_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(cell_results_path, f"cell_marker_heatmap_{tissue}.png")
            )
    for tissue, fig in cell_residual_figures_dict.items():
        if fig:
            fig.savefig(
                os.path.join(cell_results_path, f"cell_residual_plot_{tissue}.png")
            )


@click.command(help="LiquidSig: Predict tissue of origin from cfRNA transcript data.")
@click.version_option()
@click.option(
    "--transcript-quants",
    help="Transcript-level quant.sf file (e.g., from Salmon).",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    # TODO: expand to multiple with default=[]
)
# Select one of human or mouse organism via this click flag
@click.option(
    "--organism",
    help="Organism to analyze, currently limited to mouse and human (via CZI CellGuide).",
    type=click.Choice(["Homo sapiens", "Mus musculus"]),
    default="Homo sapiens",
    show_default=True,
)
# Normalization options for input data
@click.option(
    "--normalize-method",
    help="Method use to normalize input quants data.",
    type=click.Choice(["none", "log1p", "log2", "scale"]),
    default="log1p",
    show_default=True,
)
@click.option(
    "--renormalize-reference",
    help="Should we also apply normalization to the CZI data? [Experimental!]",
    is_flag=True,
    show_default=True,
)
# Optional flags
@click.option("--skip-figures", help="Don't generate figures.", is_flag=True)
@click.option(
    "--skip-cell-deconvolution", help="Skip cell-level deconvolution.", is_flag=True
)
@click.option("--verbose", help="Verbose output.", is_flag=True)
@click.option("--debug", help="Debug output.", is_flag=True)
def main(
    transcript_quants: str,
    organism: str,
    normalize_method: str,
    renormalize_reference: bool,
    skip_figures: bool,
    skip_cell_deconvolution: bool,
    verbose: bool,
    debug: bool,
) -> None:
    """Run LiquidSig cfRNA deconvolution pipeline.

    Args:
        transcript_quants: Path to transcript quantification file (e.g., Salmon quant.sf)
        organism: Target organism ("Homo sapiens" or "Mus musculus")
        normalize_method: Expression normalization method ('none', 'log1p', 'log2', 'scale')
        renormalize_reference: Whether to normalize reference data
        skip_figures: Skip figure generation.
        skip_cell_deconvolution: Skip cell-level deconvolution.
        verbose: Enable verbose output
        debug: Enable debug output and save intermediate files

    Side Effects:
        - Downloads reference data to ./references/
        - Creates output directory ./run_results/YYYY-MM-DD_HH-MM-SS/
        - Saves figures and statistics to output directory

    Raises:
        ValueError: Input cfRNA does not contain enough marker genes
    """
    time_start = time.time()

    # Print run information
    click.secho(
        f"LiquidSig: cfRNA ML-Guided Analysis (version {version('liquidsig')})",
        fg="green",
        bold=True,
    )

    # Make an output path
    run_results_path = os.path.join("run_results/", time.strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(run_results_path, exist_ok=True)
    # Make a subdirector for debug/internal data
    os.makedirs(os.path.join(run_results_path, "debug"), exist_ok=True)
    # TODO: Import logging and print output to a file, too
    # Maybe like: https://stackoverflow.com/questions/61387424/how-to-output-logs-with-python-logging-in-a-click-cli

    # Load transcript quants
    transcript_quants_df = load_transcript_quants(transcript_quants, verbose=verbose)

    # Download and cache reference data
    gencode_gtf_file, marker_file = get_references()

    # Load and preprocess marker data
    marker_data, cellgene_markers = load_marker_data(
        marker_file, organism=organism, verbose=verbose
    )

    # Load and preprocess the GTF data
    gencode_df = load_gencode_gtf(gencode_gtf_file, verbose=verbose)

    # Process our marker data to match the GTF data
    # This ensures matching gene names & also handles transcript-only input
    polished_quants_df, unannotated_quants_df = harmonize_gene_names(
        transcript_quants_df, gencode_df, verbose=verbose
    )

    # Save any unannotated quants to a file
    if len(unannotated_quants_df) > 0:
        click.secho(
            f"Warning: {len(unannotated_quants_df)} in your quants did not have maching annotations in the GTF.",
            fg="yellow",
            bold=True,
        )

        unannotated_quants_file = os.path.join(
            run_results_path, "debug/", "unannotated_quants.tsv"
        )
        unannotated_quants_df.to_csv(unannotated_quants_file, sep="\t", index=False)

        click.echo(f"\tUnannotated quants saved to {unannotated_quants_file}\n")

    # Next, let's see what marker genes are in the transcript quants
    filtered_polished_quants_df = polished_quants_df[
        polished_quants_df["gene_name"].isin(cellgene_markers)
    ]

    click.echo(f"Number of markers in CZI CellGene data: {len(cellgene_markers)}")
    click.echo(
        f"Number of those markers in your data:   {len(filtered_polished_quants_df)}"
    )
    click.secho(
        f"Percent of markers found in your data: {len(filtered_polished_quants_df) / len(cellgene_markers) * 100:.2f}%\n",
        fg="green",
        bold=True,
    )

    # Save markers for debugging
    marker_quants_file = os.path.join(
        run_results_path, "debug/", "quant_data_used_for_deconvolution.tsv"
    )
    filtered_polished_quants_df.to_csv(marker_quants_file, sep="\t", index=False)

    # Save missed markers to a file for debugging
    missed_markers = set(cellgene_markers) - set(
        filtered_polished_quants_df["gene_name"].values
    )
    missed_marker_file = os.path.join(
        run_results_path, "debug/", "cellgene_markers_not_in_your_quant_dataset.tsv"
    )
    missed_marker_df = pd.DataFrame(missed_markers, columns=["gene_name"])
    missed_marker_df.to_csv(missed_marker_file, sep="\t", index=False)

    if len(filtered_polished_quants_df) < 100:
        click.echo(
            "Not enough marker genes are represented in your cfRNA quants. Unable to deconvolute."
        )
        click.echo("Maybe your transcript/gene IDs are incorrect?")
        raise ValueError("Insufficient marker genes in quant data.")

    ## Time to deconvolute

    # Rename gene_name to GeneName in polished_quants_df
    polished_quants_df.rename(columns={"gene_name": "GeneName"}, inplace=True)

    # Now we have the polished quants and the marker data in a format that can be used for deconvolution
    # Let's run the deconvolution
    deconvolution = HierarchicalDeconvolution(
        polished_quants_df,
        marker_data,
        normalize_method=normalize_method,
        renormalize_reference=renormalize_reference,
        verbose=verbose,
    )

    (
        tissue_proportion_df,
        tissue_stats,
        tissue_figures,
        cell_proportion_df,
        cell_stats,
        cell_proportion_figures_dict,
        cell_scatter_figures_dict,
        cell_marker_heatmap_figures_dict,
        cell_residual_figures_dict,
    ) = deconvolution.run(
        skip_figures=skip_figures, skip_cell_deconvolution=skip_cell_deconvolution
    )

    print("Tissue Proportions:")
    # Instead of printing tissue_proportion_df as a table, print an ASCII bar graph:
    max_bar_length = 50
    max_value = tissue_proportion_df["Proportion"].max()
    for _, row in tissue_proportion_df.iterrows():
        proportion_pct = row["Proportion"] * 100
        bar_length = int((row["Proportion"] / max_value) * max_bar_length)
        print(
            f"{row['Tissue'][:20].ljust(20)} {proportion_pct:6.2f}% | {'#'*bar_length}"
        )

    # Save the results to a file
    tissue_proportion_df.to_csv(
        os.path.join(run_results_path, "tissue_deconvolution.csv"), index=False
    )

    tissue_stats_df = pd.DataFrame.from_dict(tissue_stats, orient="index").transpose()
    tissue_stats_df.to_csv(
        os.path.join(run_results_path, "tissue_deconvolution_stats.csv"), index=False
    )

    # Also save the cell deconvolution results
    if not skip_cell_deconvolution:
        # Put cell deconvolution results in a subdirectory
        cell_results_path = os.path.join(run_results_path, "cell")
        os.makedirs(cell_results_path, exist_ok=True)

        cell_proportion_df.to_csv(
            os.path.join(cell_results_path, "cell_deconvolution.csv"), index=False
        )

        cell_stats_df = pd.DataFrame.from_dict(cell_stats, orient="index").transpose()
        cell_stats_df.to_csv(
            os.path.join(cell_results_path, "cell_deconvolution_stats.csv"), index=False
        )

    if not skip_figures:
        export_tissue_figures(run_results_path, tissue_figures)

        if not skip_cell_deconvolution:
            export_cell_figures(
                cell_results_path,
                cell_proportion_figures_dict,
                cell_scatter_figures_dict,
                cell_marker_heatmap_figures_dict,
                cell_residual_figures_dict,
            )

    # Summarize our run
    click.echo(f"Output saved to: {run_results_path}\n")
    click.secho("Warning: This is an *Alpha* implementation!", fg="green", bold=True)

    elapsed_time = time.time() - time_start
    minutes, seconds = divmod(int(elapsed_time), 60)
    click.echo(f"\nTime elapsed: {minutes}m {seconds}s")


if __name__ == "__main__":
    main.main(
        standalone_mode=False,
        args=[
            "--transcript-quants",
            "../quants-trial/quant.genes.sf",
            "--organism",
            "Homo sapiens",
            "--verbose",
            "--debug",
        ],
    )  # pragma: no cover
