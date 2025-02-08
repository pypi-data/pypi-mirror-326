"""
Perform hierarchical deconvolution of cfRNA data to estimate tissue and cell type proportions.

This module implements a two-stage deconvolution approach:
1. Tissue-level deconvolution using tissue-specific marker genes
2. Cell-type deconvolution within each tissue using cell-specific markers

The implementation supports various normalization methods to handle differences between
RNA-seq TPM values and reference expression data.
"""

# Third party modules
from cellxgene_ontology_guide.ontology_parser import OntologyParser
import pandas as pd
import numpy as np
from scipy.optimize import nnls
from scipy.stats import pearsonr
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


matplotlib.rcParams["figure.max_open_warning"] = (
    0  # Suppress warning about too many open figures
)


class HierarchicalDeconvolution:
    """Perform hierarchical deconvolution of cfRNA data.

    This class implements a two-stage deconvolution process to estimate both tissue
    and cell-type proportions from cfRNA data. It handles data normalization,
    marker gene selection, and visualization of results.

    Attributes:
        mixture_data (pd.DataFrame): Input mixture cfRNA data
        training_data (pd.DataFrame): Reference expression data
        tissue_proportion_df (pd.DataFrame | None): Results of tissue deconvolution
        tissue_stats (dict[str, float]): Quality metrics for tissue deconvolution
        tissue_figures (dict[str, plt.Figure]): Visualization figures for tissue results
        cell_proportion_df (pd.DataFrame | None): Results of cell deconvolution
        cell_stats (dict[str, dict[str, float]]): Quality metrics for cell deconvolution by tissue
        cell_proportion_figures_dict (dict[str, plt.Figure | None]): Cell proportion figures by tissue
    """

    def __init__(
        self,
        mixture_data: pd.DataFrame,
        training_data: pd.DataFrame,
        top_tissue_markers: int = 100,
        top_cell_markers: int = 100,
        normalize_method: str = "log1p",  # Options: 'none', 'log1p', 'log2', 'scale'
        renormalize_reference: bool = False,
        verbose: bool = False,
    ) -> None:
        """Initialize the deconvolution pipeline.

        Args:
            mixture_data: RNA-seq data with columns 'GeneName' and 'TPM'
            training_data: Reference data with columns ['Tissue', 'Cell', 'GeneName',
                         'GeneMarkerScore', 'GeneMeanExpression', 'GenePercentExpressing']
            top_tissue_markers: Number of marker genes for tissue deconvolution
            top_cell_markers: Number of marker genes for cell deconvolution
            normalize_method: Data normalization method ('none', 'log1p', 'log2', 'scale')
            renormalize_reference: Whether to also normalize reference data
            verbose: Print detailed progress information

        Raises:
            AssertionError: If input parameters are invalid
        """

        self.mixture_data = mixture_data
        self.training_data = training_data
        self.top_tissue_markers = top_tissue_markers
        self.top_cell_markers = top_cell_markers
        self.normalize_method = normalize_method
        self.renormalize_reference = renormalize_reference
        self.verbose = verbose

        # Ontology parser & lookup dict for cell names
        self.ontology_parser = None
        self._cell_name_lookup = {}

        # Validate input data
        assert isinstance(self.mixture_data, pd.DataFrame)
        assert isinstance(self.training_data, pd.DataFrame)
        assert self.top_cell_markers > 0
        assert self.top_tissue_markers > 0

        self.validate_deconvolution_input()

        self.tissue_list = self.training_data["Tissue"].unique()

        # Convert mixture data to a dict for efficient lookups:
        self.mixture_data_dict = self.mixture_data.set_index("GeneName")[
            "TPM"
        ].to_dict()

        # Store results
        self.tissue_proportion_df = None

        self.tissue_internals = {
            "tissue_marker_expression_df": None,
            "mixture_tissue_expression_vector": None,
            "reconstructed_tissue_expression": None,
        }

        self.tissue_stats: dict[str, float] = {}

        self.tissue_figures = {
            "proportion": None,
            "scatter": None,
            "marker_heatmap": None,
            "residual": None,
        }

        # Store the results of cell deconvolution in a single df
        self.cell_proportion_df = None

        # TODO: Change this dict to have tissue be the key?
        self.cell_stats: dict[str, dict[str, float]] = {
            "r2": {},
            "rmse": {},
            "pearson_r": {},
        }

        # This is a dict of each cell type, each of which contains a dict of internals
        self.cell_internals: dict[str, dict] = {}

        self.cell_proportion_figures_dict: dict[str, plt.Figure | None] = {}
        self.cell_scatter_figures_dict: dict[str, plt.Figure | None] = {}
        self.cell_marker_heatmap_figures_dict: dict[str, plt.Figure | None] = {}
        self.cell_residual_figures_dict: dict[str, plt.Figure | None] = {}

    def validate_deconvolution_input(self):
        """
        Validate the input data for deconvolution.

        Raises:
            ValueError: If required columns are missing in the input data.
        """

        required_columns_mixture = ["GeneName", "TPM"]
        if not set(required_columns_mixture).issubset(self.mixture_data.columns):
            raise ValueError(
                f"Mixture data must contain columns: {required_columns_mixture}"
            )

        required_columns_training = [
            "Tissue",
            "Cell",
            "GeneName",
            "GeneMarkerScore",
            "GeneMeanExpression",
            "GenePercentExpressing",
        ]
        if not set(required_columns_training).issubset(self.training_data.columns):
            raise ValueError(
                f"Training data must contain columns: {required_columns_training}"
            )

    def _normalize_expression_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize expression data using the specified method.

        Args:
            data: Raw expression data array

        Returns:
            Normalized expression data array

        Raises:
            ValueError: If normalize_method is invalid
        """
        if self.verbose:
            print(f"\tNormalizing data using method: {self.normalize_method}")
        if self.normalize_method == "none":
            return data
        elif self.normalize_method == "log1p":
            return np.log1p(data)
        elif self.normalize_method == "log2":
            # Add small epsilon to avoid log(0)
            return np.log2(data + 1e-10)
        elif self.normalize_method == "scale":
            # Scale to [0,1] range
            if np.max(data) == np.min(data):
                return data
            return (data - np.min(data)) / (np.max(data) - np.min(data))
        else:
            raise ValueError(f"Unknown normalization method: {self.normalize_method}")

    def tissue_level_deconvolution(self):
        """
        Perform tissue-level deconvolution using marker genes from the training data.

        This method:
        1. Identifies top marker genes for each tissue
        2. Creates reference expression matrices
        3. Performs non-negative least squares optimization
        4. Calculates tissue proportions and quality metrics

        The results are stored in class attributes:
        - tissue_proportion_df: DataFrame with tissue proportions
        - tissue_stats: Dictionary containing r2, rmse, and pearson_r statistics
        - tissue_internals: Dictionary containing intermediate calculation results

        Raises:
            ValueError: If no overlapping marker genes are found between training and mixture data
        """
        print("Starting tissue-level deconvolution...")

        print(f"\tNumber of Tissues: {len(self.tissue_list)}")
        tissue_marker_expression_profiles = {}
        tissue_markers = {}

        # Subset to the top marker genes for each tissue (based on top_tissue_markers)
        for tissue in self.tissue_list:
            tissue_specific_markers = (
                self.training_data[self.training_data["Tissue"] == tissue]
                .sort_values("GeneMarkerScore", ascending=False)
                .drop_duplicates(subset=["GeneName"])
            )

            top_markers = tissue_specific_markers.head(self.top_tissue_markers)
            tissue_markers[tissue] = top_markers["GeneName"].tolist()
            tissue_marker_expression_profiles[tissue] = top_markers.set_index(
                "GeneName"
            )["GeneMeanExpression"].to_dict()

        # Ensure we have overlap of the top marker genes between training and mixture data
        tissue_marker_genes = list(
            set(gene for markers in tissue_markers.values() for gene in markers)
        )
        tissue_marker_genes_intersection = list(
            set(tissue_marker_genes) & set(self.mixture_data["GeneName"])
        )
        if not tissue_marker_genes_intersection:
            raise ValueError(
                "No overlapping marker genes found between training and mixture data for tissue deconvolution."
            )

        # Prepare the reference tissue expression matrix
        reference_tissue_expression = []
        tissue_names_for_matrix = []
        for tissue in self.tissue_list:
            profile = tissue_marker_expression_profiles[tissue]
            expression_vector = [
                profile.get(gene, 0) for gene in tissue_marker_genes_intersection
            ]
            reference_tissue_expression.append(expression_vector)
            tissue_names_for_matrix.append(tissue)

        # Prepare the matrices for constrained least squares
        if self.renormalize_reference:
            print("* EXPERIMENTAL: Renormalizing reference tissue expression data.")
            reference_tissue_expression_matrix = self._normalize_expression_data(
                np.array(reference_tissue_expression).T
            )
        else:
            reference_tissue_expression_matrix = np.array(reference_tissue_expression).T

        # Extract the mixture expression vector for the marker genes, filling with 0 if gene not present
        self.tissue_internals["mixture_tissue_expression_vector"] = (
            self._normalize_expression_data(
                np.array(
                    [
                        (
                            self.mixture_data_dict[gene]
                            if gene in self.mixture_data_dict
                            else 0
                        )
                        for gene in tissue_marker_genes_intersection
                    ]
                )
            )
        )

        self.tissue_internals["tissue_marker_expression_df"] = pd.DataFrame(
            reference_tissue_expression_matrix,
            index=tissue_marker_genes_intersection,
            columns=tissue_names_for_matrix,
        )

        # Constrained Least Squares for Tissue Deconvolution
        # NNLS seems to outperform L-BFGS-B and SLSQP for our use case
        tissue_proportions, residual_norm = nnls(
            reference_tissue_expression_matrix,
            self.tissue_internals["mixture_tissue_expression_vector"],
        )
        tissue_proportions_normalized = (
            tissue_proportions / tissue_proportions.sum()
            if tissue_proportions.sum() > 0
            else tissue_proportions
        )

        # Use the NNLS residual_norm to calculate the proportion of unexplained variance -- this is not the same as R-squared, but a useful metric for NNLS
        # Note we are not comparing the same values -- specifically we have TPM data from our mixture, but mean expression data from our training data
        # TODO: Consider normalizing the data before calculating residual_norm or fitting the model?
        total_variance = np.sum(
            (
                self.tissue_internals["mixture_tissue_expression_vector"]
                - np.mean(self.tissue_internals["mixture_tissue_expression_vector"])
            )
            ** 2
        )
        if total_variance == 0:
            proportion_unexplained_variance = 0
        else:
            unexplained_variance = np.sum(residual_norm**2)
            proportion_unexplained_variance = unexplained_variance / total_variance
        if self.verbose:
            print(
                f"\tProportion of Unexplained Variance: {proportion_unexplained_variance:.3f}"
            )

        tissue_proportion_df = pd.DataFrame(
            {
                "Tissue": tissue_names_for_matrix,
                "Proportion": tissue_proportions_normalized,
            }
        )

        # Calculate Statistics for tissue deconvolution
        self.tissue_internals["reconstructed_tissue_expression"] = (
            reference_tissue_expression_matrix @ tissue_proportions
        )
        tissue_r2 = r2_score(
            self.tissue_internals["mixture_tissue_expression_vector"],
            self.tissue_internals["reconstructed_tissue_expression"],
        )
        tissue_rmse = np.sqrt(
            mean_squared_error(
                self.tissue_internals["mixture_tissue_expression_vector"],
                self.tissue_internals["reconstructed_tissue_expression"],
            )
        )
        tissue_pearson_r, _ = pearsonr(
            self.tissue_internals["mixture_tissue_expression_vector"],
            self.tissue_internals["reconstructed_tissue_expression"],
        )

        # Store results
        self.tissue_proportion_df = tissue_proportion_df
        self.tissue_stats["r2"] = tissue_r2
        self.tissue_stats["rmse"] = tissue_rmse
        self.tissue_stats["pearson_r"] = tissue_pearson_r

        for metric, value in self.tissue_stats.items():
            print(f"\t{metric.upper()}: {value:.3f}")
        print()

        print("Completed tissue deconvolution.\n")

    def _get_cell_name(self, cell_id: str) -> str:
        """
        Return the cell name for a given cell ID.

        Args:
            cell_id: Cell ID

        Returns:
            Cell name
        """
        if not self.ontology_parser:
            self.ontology_parser = OntologyParser(schema_version="v5.3.0")

        if cell_id not in self._cell_name_lookup:
            self._cell_name_lookup[cell_id] = self.ontology_parser.get_term_label(
                cell_id
            )

        return self._cell_name_lookup[cell_id]

    def cell_level_deconvolution(self):
        """
        Perform cell-level deconvolution within each tissue using marker genes.

        This method performs deconvolution for each tissue separately to estimate
        the proportions of different cell types within that tissue. Results are stored
        in class attributes:
        - cell_proportion_df: DataFrame with columns 'Tissue', 'Cell', and 'Proportion'
        - cell_stats: Dictionary containing r2, rmse, and pearson_r statistics per tissue
        - cell_internals: Dictionary containing intermediate calculation results per tissue

        The method handles cases where marker genes may not be present in the mixture data
        and skips tissues where deconvolution cannot be performed.

        Note:
            Cell proportions are normalized within each tissue independently.
        """
        print("Starting cell-level deconvolution...")

        for tissue in self.tissue_list:
            if self.verbose:
                print(f"Cell-level deconvoluting: {tissue}")

            # We store the internals of each cell-level deconvolution, but since the same cell type
            # can exist in multiple different tissues (with different internals), we need a nested dict.
            self.cell_internals[tissue] = {}

            self.cell_internals[tissue]["cells_in_tissue"] = self.training_data[
                self.training_data["Tissue"] == tissue
            ]["Cell"].unique()

            # Let's get the top marker genes & their expression profiles for each cell type in this tissue
            cell_marker_expression_profiles = {}
            cell_markers = {}

            for cell in self.cell_internals[tissue]["cells_in_tissue"]:
                # Add the internals for this cell to the nested dict

                cell_specific_markers = (
                    self.training_data[
                        (self.training_data["Tissue"] == tissue)
                        & (self.training_data["Cell"] == cell)
                    ]
                    .sort_values("GeneMarkerScore", ascending=False)
                    .drop_duplicates(subset=["GeneName"])
                )

                top_markers = cell_specific_markers.head(self.top_cell_markers)
                cell_markers[cell] = top_markers["GeneName"].tolist()
                cell_marker_expression_profiles[cell] = top_markers.set_index(
                    "GeneName"
                )["GeneMeanExpression"].to_dict()

            cell_marker_genes = list(
                set(gene for markers in cell_markers.values() for gene in markers)
            )

            cell_marker_genes_intersection = list(
                set(cell_marker_genes) & set(self.mixture_data["GeneName"])
            )

            # TODO: Think if it's even possible to have no overlapping marker genes
            if not cell_marker_genes_intersection:
                print(
                    f"Warning: No overlapping marker genes found for cell deconvolution in Tissue: {tissue}. Skipping this tissue."
                )
                self.cell_internals[tissue]["cell_proportions_dict"] = pd.DataFrame(
                    {
                        "Tissue": [tissue],
                        "Cell": self.cell_internals[tissue]["cells_in_tissue"],
                        "Proportion": np.nan,
                    }
                )
                self.cell_stats[tissue] = {
                    "r2": np.nan,
                    "rmse": np.nan,
                    "pearson_r": np.nan,
                }
                continue

            reference_cell_expression = []
            for cell in self.cell_internals[tissue]["cells_in_tissue"]:
                profile = cell_marker_expression_profiles[cell]
                expression_vector = [
                    profile.get(gene, 0) for gene in cell_marker_genes_intersection
                ]
                reference_cell_expression.append(expression_vector)

            # Prepare the reference cell expression matrix
            if self.renormalize_reference:
                print("* EXPERIMENTAL: Renormalizing reference cell expression data.")
                reference_cell_expression_matrix = self._normalize_expression_data(
                    np.array(reference_cell_expression).T
                )
            else:
                reference_cell_expression_matrix = np.array(reference_cell_expression).T

            self.cell_internals[tissue][
                "reference_cell_expression_matrix"
            ] = reference_cell_expression_matrix

            # Store this as a DataFrame for visualization later on
            self.cell_internals[tissue]["cell_marker_expression_df"] = pd.DataFrame(
                reference_cell_expression_matrix,
                index=cell_marker_genes_intersection,
                columns=self.cell_internals[tissue]["cells_in_tissue"],
            )

            mixture_cell_expression_vector = self._normalize_expression_data(
                np.array(
                    [
                        (
                            self.mixture_data_dict[gene]
                            if gene in self.mixture_data_dict
                            else 0
                        )
                        for gene in cell_marker_genes_intersection
                    ]
                )
            )
            self.cell_internals[tissue][
                "mixture_cell_expression_vector"
            ] = mixture_cell_expression_vector

            # Constrained Least Squares for Cell Deconvolution
            cell_proportions, _ = nnls(
                reference_cell_expression_matrix, mixture_cell_expression_vector
            )
            cell_proportions_normalized = (
                cell_proportions / cell_proportions.sum()
                if cell_proportions.sum() > 0
                else cell_proportions
            )

            self.cell_internals[tissue]["cell_proportions_dict"] = pd.DataFrame(
                {
                    "Tissue": [tissue]
                    * len(self.cell_internals[tissue]["cells_in_tissue"]),
                    "Cell": self.cell_internals[tissue]["cells_in_tissue"],
                    "Proportion": cell_proportions_normalized,
                }
            )

            self.cell_internals[tissue]["cell_proportions_dict"]["CellName"] = (
                self.cell_internals[tissue]["cell_proportions_dict"]["Cell"].apply(
                    self._get_cell_name
                )
            )

            # Calculate Statistics for cell-level deconvolution
            reconstructed_cell_expression = (
                reference_cell_expression_matrix @ cell_proportions
            )
            self.cell_internals[tissue][
                "reconstructed_cell_expression"
            ] = reconstructed_cell_expression
            self.cell_stats[tissue] = {}

            self.cell_stats[tissue]["r2"] = r2_score(
                mixture_cell_expression_vector, reconstructed_cell_expression
            )
            self.cell_stats[tissue]["rmse"] = np.sqrt(
                mean_squared_error(
                    mixture_cell_expression_vector, reconstructed_cell_expression
                )
            )
            self.cell_stats[tissue]["pearson_r"], _ = pearsonr(
                mixture_cell_expression_vector, reconstructed_cell_expression
            )

            if self.verbose:
                # Print our stats
                print("\t", end="")
                print(
                    ", ".join(
                        [
                            f"{metric.upper()}: {value:.3f}"
                            for metric, value in self.cell_stats[tissue].items()
                        ]
                    )
                )
                print()

        # Aggregate all of the different tissues in self.cell_internals[tissue]['cell_proportions_dict'] into a single DataFrame
        self.cell_proportion_df = pd.concat(
            [
                self.cell_internals[tissue]["cell_proportions_dict"]
                for tissue in self.tissue_list
            ]
        )

        print("Cell deconvolutions complete.")

    def generate_tissue_figures(self):
        """
        Generate visualization figures for tissue-level deconvolution results.

        Creates and stores the following figures in the tissue_figures dictionary:
        - proportion: Bar plot of estimated tissue proportions
        - scatter: Scatter plot of reconstructed vs original expression
        - marker_heatmap: Heatmap of marker gene expression across tissues
        - residual: Residual plot for quality assessment

        Each figure is stored as a matplotlib Figure object in the tissue_figures
        dictionary using the corresponding key.
        """
        # Tissue Proportion Bar Plot (same as before)
        tissue_fig_prop, ax_tissue_prop = plt.subplots(figsize=(10, 12))
        sns.barplot(
            x="Proportion",
            y="Tissue",
            data=self.tissue_proportion_df.sort_values("Proportion", ascending=False),
            hue="Tissue",
            dodge=False,
            legend=False,
            palette="viridis",
            ax=ax_tissue_prop,
        )
        ax_tissue_prop.set_title("Estimated Tissue Proportions")
        ax_tissue_prop.set_xlabel("Proportion")
        ax_tissue_prop.set_ylabel("Tissue")
        tissue_fig_prop.tight_layout()
        self.tissue_figures["proportion"] = tissue_fig_prop

        # Tissue Scatter Plot (Reconstructed vs. Original)
        tissue_fig_scatter, ax_tissue_scatter = plt.subplots(figsize=(8, 8))
        sns.scatterplot(
            x=self.tissue_internals["mixture_tissue_expression_vector"],
            y=self.tissue_internals["reconstructed_tissue_expression"],
            ax=ax_tissue_scatter,
        )
        ax_tissue_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
        ax_tissue_scatter.set_ylabel("Reconstructed Tissue Expression (Marker Genes)")
        ax_tissue_scatter.set_title("Tissue Deconvolution: Reconstructed vs. Original")
        ax_tissue_scatter.plot(
            [
                min(self.tissue_internals["mixture_tissue_expression_vector"]),
                max(self.tissue_internals["mixture_tissue_expression_vector"]),
            ],
            [
                min(self.tissue_internals["mixture_tissue_expression_vector"]),
                max(self.tissue_internals["mixture_tissue_expression_vector"]),
            ],
            color="red",
            linestyle="--",
        )  # Diagonal line
        tissue_fig_scatter.tight_layout()
        self.tissue_figures["scatter"] = tissue_fig_scatter

        # Tissue Marker Heatmap
        tissue_marker_heatmap_fig, ax_tissue_heatmap = plt.subplots(figsize=(10, 10))
        sns.heatmap(
            self.tissue_internals["tissue_marker_expression_df"],
            cmap="viridis",
            ax=ax_tissue_heatmap,
            cbar_kws={"label": "Mean Expression"},
        )
        ax_tissue_heatmap.set_title("Tissue Marker Gene Expression Heatmap")
        ax_tissue_heatmap.set_xlabel("Tissues")
        ax_tissue_heatmap.set_ylabel("Marker Genes")
        tissue_marker_heatmap_fig.tight_layout()
        self.tissue_figures["marker_heatmap"] = tissue_marker_heatmap_fig

        # Tissue Residual Plot
        tissue_fig_residual, ax_tissue_residual = plt.subplots(figsize=(8, 8))
        residuals_tissue = (
            self.tissue_internals["reconstructed_tissue_expression"]
            - self.tissue_internals["mixture_tissue_expression_vector"]
        )
        sns.scatterplot(
            x=self.tissue_internals["mixture_tissue_expression_vector"],
            y=residuals_tissue,
            ax=ax_tissue_residual,
        )
        ax_tissue_residual.axhline(0, color="red", linestyle="--")  # Zero line
        ax_tissue_residual.set_xlabel("Original Mixture Expression (Marker Genes)")
        ax_tissue_residual.set_ylabel("Residuals (Reconstructed - Original)")
        ax_tissue_residual.set_title("Tissue Deconvolution: Residual Plot")
        tissue_fig_residual.tight_layout()
        self.tissue_figures["residual"] = tissue_fig_residual

        print("Tissue figures generated.")

    def generate_cell_figures(self):
        """
        Generate visualization figures for cell-level deconvolution results.

        Creates separate figures for each tissue, storing them in dictionaries:
        - cell_proportion_figures_dict: Bar plots of cell proportions per tissue
        - cell_scatter_figures_dict: Scatter plots of reconstructed vs original expression
        - cell_marker_heatmap_figures_dict: Heatmaps of marker gene expression
        - cell_residual_figures_dict: Residual plots for quality assessment
        """
        print("Generating cell figures...")
        cell_proportion_figures_dict = {}
        cell_scatter_figures_dict = {}
        cell_marker_heatmap_figures_dict = {}
        cell_residual_figures_dict = {}

        for tissue in self.tissue_list:
            if self.verbose:
                print(f"\t{tissue}")
            cell_props_tissue = self.cell_internals[tissue]["cell_proportions_dict"]
            if (
                cell_props_tissue is not None
                and not cell_props_tissue["Proportion"].isnull().all()
            ):
                cell_props_tissue_valid = cell_props_tissue.dropna(
                    subset=["Proportion"]
                ).sort_values("Proportion", ascending=False)

                # Cell Proportion Bar Plot
                cell_fig_prop, ax_cell_prop = plt.subplots(figsize=(8, 8))
                sns.barplot(
                    x="Proportion",
                    y="CellName",
                    data=cell_props_tissue_valid,
                    hue="CellName",
                    dodge=False,
                    legend=False,
                    palette="viridis",
                    ax=ax_cell_prop,
                )
                ax_cell_prop.set_title(f"Cell Proportions within {tissue} Tissue")
                ax_cell_prop.set_xlabel("Proportion")
                ax_cell_prop.set_ylabel("Cell Type")
                cell_fig_prop.tight_layout()
                cell_proportion_figures_dict[tissue] = cell_fig_prop

                # Cell Scatter Plot (Reconstructed vs. Original)
                cell_fig_scatter, ax_cell_scatter = plt.subplots(figsize=(8, 8))

                sns.scatterplot(
                    x=self.cell_internals[tissue]["mixture_cell_expression_vector"],
                    y=self.cell_internals[tissue]["reconstructed_cell_expression"],
                    ax=ax_cell_scatter,
                )
                ax_cell_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
                ax_cell_scatter.set_ylabel(
                    "Reconstructed Cell Expression (Marker Genes)"
                )
                ax_cell_scatter.set_title(
                    f"Cell Deconvolution in {tissue}: Reconstructed vs. Original"
                )
                ax_cell_scatter.plot(
                    [
                        min(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                        max(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                    ],
                    [
                        min(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                        max(
                            self.cell_internals[tissue][
                                "mixture_cell_expression_vector"
                            ]
                        ),
                    ],
                    color="red",
                    linestyle="--",
                )  # Diagonal line
                cell_fig_scatter.tight_layout()
                cell_scatter_figures_dict[tissue] = cell_fig_scatter

                # Cell Marker Heatmap
                cell_marker_heatmap_fig, ax_cell_heatmap = plt.subplots(figsize=(8, 8))
                self.cell_internals[tissue]["cell_marker_expression_df"].columns = [
                    self._get_cell_name(c)
                    for c in self.cell_internals[tissue][
                        "cell_marker_expression_df"
                    ].columns
                ]
                sns.heatmap(
                    self.cell_internals[tissue]["cell_marker_expression_df"],
                    cmap="viridis",
                    ax=ax_cell_heatmap,
                    cbar_kws={"label": "Mean Expression"},
                )
                ax_cell_heatmap.set_title(
                    f"Cell Marker Gene Expression Heatmap in {tissue}"
                )
                ax_cell_heatmap.set_xlabel("Cell Types")
                ax_cell_heatmap.set_ylabel("Marker Genes")
                cell_marker_heatmap_fig.tight_layout()
                cell_marker_heatmap_figures_dict[tissue] = cell_marker_heatmap_fig

                # Cell Residual Plot
                cell_fig_residual, ax_cell_residual = plt.subplots(figsize=(8, 8))
                residuals_cell = (
                    self.cell_internals[tissue]["reconstructed_cell_expression"]
                    - self.cell_internals[tissue]["mixture_cell_expression_vector"]
                )
                sns.scatterplot(
                    x=self.cell_internals[tissue]["mixture_cell_expression_vector"],
                    y=residuals_cell,
                    ax=ax_cell_residual,
                )
                ax_cell_residual.axhline(0, color="red", linestyle="--")  # Zero line
                ax_cell_residual.set_xlabel(
                    "Original Mixture Expression (Marker Genes)"
                )
                ax_cell_residual.set_ylabel("Residuals (Reconstructed - Original)")
                ax_cell_residual.set_title(
                    f"Cell Deconvolution in {tissue}: Residual Plot"
                )
                cell_fig_residual.tight_layout()
                cell_residual_figures_dict[tissue] = cell_fig_residual

            else:
                cell_proportion_figures_dict[tissue] = None
                cell_scatter_figures_dict[tissue] = None
                cell_marker_heatmap_figures_dict[tissue] = None
                cell_residual_figures_dict[tissue] = None

        self.cell_proportion_figures_dict = cell_proportion_figures_dict
        self.cell_scatter_figures_dict = cell_scatter_figures_dict
        self.cell_marker_heatmap_figures_dict = cell_marker_heatmap_figures_dict
        self.cell_residual_figures_dict = cell_residual_figures_dict

        print("\nCell figures generated.")

    def run(
        self,
        skip_figures: bool = False,
        skip_cell_deconvolution: bool = False,
    ) -> tuple[
        pd.DataFrame,  # tissue_proportion_df
        dict[str, float],  # tissue_stats
        dict[str, plt.Figure],  # tissue_figures
        pd.DataFrame,  # cell_proportion_df
        dict[str, dict[str, float]],  # cell_stats
        dict[str, plt.Figure | None],  # cell_proportion_figures_dict
        dict[str, plt.Figure | None],  # cell_scatter_figures_dict
        dict[str, plt.Figure | None],  # cell_marker_heatmap_figures_dict
        dict[str, plt.Figure | None],  # cell_residual_figures_dict,
    ]:
        """Execute the complete hierarchical deconvolution pipeline.

        Args:
            skip_figures: Skip generation of visualization figures
            skip_cell_deconvolution: Skip cell-level deconvolution

        Returns:
            A tuple containing:
            - tissue_proportion_df: Tissue proportions with columns ['Tissue', 'Proportion']
            - tissue_stats: Statistics including 'r2', 'rmse', 'pearson_r'
            - tissue_figures: Visualization figures for tissue results
            - cell_proportion_df: Cell proportions with columns ['Tissue', 'Cell', 'Proportion']
            - cell_stats: Cell deconvolution statistics by tissue
            - cell_proportion_figures_dict: Bar plots of cell proportions by tissue
            - cell_scatter_figures_dict: Scatter plots of reconstructed vs original expression
            - cell_marker_heatmap_figures_dict: Heatmaps of marker gene expression
            - cell_residual_figures_dict: Residual plots for quality assessment
        """

        self.validate_deconvolution_input()

        self.tissue_level_deconvolution()

        if not skip_cell_deconvolution:
            self.cell_level_deconvolution()

        if not skip_figures:
            self.generate_tissue_figures()

            if not skip_cell_deconvolution:
                self.generate_cell_figures()

        # TODO: Fix this return mess.
        return (
            self.tissue_proportion_df,
            self.tissue_stats,
            self.tissue_figures,
            self.cell_proportion_df,
            self.cell_stats,
            self.cell_proportion_figures_dict,
            self.cell_scatter_figures_dict,
            self.cell_marker_heatmap_figures_dict,
            self.cell_residual_figures_dict,
        )  # type: ignore
