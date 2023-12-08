from typing import Any, Dict, List

from utils import convert_dataframe_to_array
from dashboard import Dashboard

class Top3(Dashboard):
    """
    This path is responsible for rendering the Top 3 page.
    """

    def __init__(self, self_board: Dashboard) -> None:
        """
        Initializes the Top3 path with a shimoku client instance.

        Parameters:
            self_board (Dashboard): An instance of the Dashboard class.
        """
        super().__init__(self_board.shimoku)
        self.df_app = self_board.df_app
        self.df_app2 = self_board.df_app2
        self.df_app3 = self_board.df_app3

        self.order = 0  # Initialize order of plotting elements
        self.menu_path = "Top 3"  # Set the menu path for this page

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def plot(self, title: str, subtitle: str) -> bool:
        """
        Plots the Top 3 page.

        Parameters:
            title (str): The title of the page.
            subtitle (str): The subtitle of the page.

        Returns:
            bool: True if plotting is successful.
        """
        self.plotHeader(title, subtitle)
        self.plot_kpi_indicators()
        return True

    def plot_kpi_indicators(self) -> None:
        """
        Plots the Key Performance Indicators (KPIs) for the Top 3 page.
        """
        self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app["main_kpis"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app["main_kpis"]) + 1

        self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app2["main_kpis2"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app2["main_kpis2"]) + 1

        self.shimoku.plt.indicator(
            data=convert_dataframe_to_array(self.df_app3["main_kpis3"]),
            order=self.order,
            rows_size=1,
            cols_size=12,
            value="value",
            header="title",
            footer="description",
            color="color",
            align="align",
        )
        self.order += len(self.df_app3["main_kpis3"]) + 1

    def plotHeader(self, title: str, subtitle: str) -> None:
        """
        Plots the header of the Top 3 page.

        Parameters:
            title (str): The title of the page.
            subtitle (str): The subtitle of the page.
        """
        self.shimoku.plt.html(
            order=self.order,
            html=self.shimoku.html_components.create_h1_title(
                title=title,
                subtitle=subtitle
            )
        )
        self.order += 1
