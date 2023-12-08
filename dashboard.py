import pandas as pd
from shimoku_api_python import Client
import utils  # Assuming utils.py contains the required utility functions


class Dashboard:
    def __init__(self, shimoku: Client) -> None:
        """
        Initializes the Dashboard object.

        Parameters:
        - shimoku (Client): An instance of the Shimoku client.

        Returns:
        - None
        """
        self.order = 0
        self.shimoku = shimoku
        self.dashboardName = "Video Games Sales"
        self.fileNames = ["./data/Video_Games_Sales_as_at_22_Dec_2016.csv"]
        self.dfs = utils.getData(self.fileNames)

    def __str__(self) -> str:
        """
        Returns a string representation of the Dashboard.

        Returns:
        - str: String representation of the Dashboard.
        """
        return f"Dashboard {self.dashboardName}"

    def setDashboard(self) -> None:
        """
        Sets up the Shimoku dashboard with various visualizations.

        Returns:
        - None
        """
        self.shimoku.set_board(self.dashboardName)
        self.shimoku.set_menu_path(name="Video Game Sales Report")

        self.plotHeader("Overview")

        self.plotData("Genre")
        self.plotReleasesYearRelease()
        self.plotSalesYearRelease("Genre")
        self.plotGenres()

        self.plotData("Platform")
        self.plotSalesYearRelease("Platform")

        self.plotTop3()

        #self.plotTop3("Platform")

    def plotHeader(self, title: str) -> None:
        """
        Plots the header of the dashboard.

        Parameters:
        - title (str): The title of the dashboard.

        Returns:
        - None
        """
        self.shimoku.plt.html(
            order=self.order,
            html=self.shimoku.html_components.create_h1_title(
                title="Video Game Sales Report",
                subtitle="A report of video game sales across various platforms, genres, and years. The data was collected by web scraping Metacritic from 1980 to 2016",
            ),
        )
        self.order += 1

    def plotReleasesYearRelease(self) -> None:
        """
        Plots a stacked bar chart for games by the year of release.

        Returns:
        - None
        """
        dfVG_Sales = self.dfs["Video_Games_Sales_as_at_22_Dec_2016"]
        releasesPerYear = utils.groupingByYearCount(dfVG_Sales, "Genre")
        self.shimoku.plt.stacked_bar(
            data=releasesPerYear,
            x="Year_of_Release",
            x_axis_name="Year of Release",
            order=self.order,
            rows_size=2,
            cols_size=5,
            padding="0,0,0,1",
            show_values=["Genre"],
            title="Games by the Year of Release",
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )
        self.order += 1

        releasesPerYear = utils.groupingByYearCountPercetange(dfVG_Sales, "Genre")
        self.shimoku.plt.stacked_bar(
            data=releasesPerYear,
            x="Year_of_Release",
            x_axis_name="Year of Release",
            order=self.order,
            rows_size=2,
            cols_size=5,
            padding="0,1,0,0",
            show_values=["Genre"],
            title="Games by the Year of Release %",
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )
        self.order += 1

    def plotSalesYearRelease(self, column: str) -> None:
        """
        Plots stacked bar charts for sales by the year of release and sales percentage.

        Returns:
        - None
        """
        dfVG_Sales = self.dfs["Video_Games_Sales_as_at_22_Dec_2016"]
        salesPerYearRelease = utils.groupingByYearSales(dfVG_Sales, column)
        self.shimoku.plt.stacked_bar(
            data=salesPerYearRelease,
            x="Year_of_Release",
            x_axis_name="Year of Release",
            order=self.order,
            rows_size=2,
            cols_size=5,
            padding="0,0,0,1",
            show_values=[column],
            title=f"Sales of Every {column} by the Year of Release",
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )
        self.order += 1

        salesPerYearReleasePercentage = utils.groupingByYearSalesPercetange(
            dfVG_Sales, column
        )
        self.shimoku.plt.stacked_bar(
            data=salesPerYearReleasePercentage,
            x="Year_of_Release",
            x_axis_name="Year of Release",
            order=self.order,
            rows_size=2,
            cols_size=5,
            padding="0,1,0,0",
            show_values=[column],
            title=f"Sales of Every {column} by the Year of Release %",
            option_modifications={
                "dataZoom": {"show": True},
                "toolbox": {"show": True},
            },
        )
        self.order += 1

    def plotData(self, column: str) -> None:
        """
        Plots KPIs (Key Performance Indicators) for the given dataset.

        Parameters:
        - column (str): The column for which KPIs are to be plotted.

        Returns:
        - None
        """
        dfVG_Sales = self.dfs["Video_Games_Sales_as_at_22_Dec_2016"]
        data = utils.getKPIs(dfVG_Sales, column)
        self.shimoku.plt.indicator(
            data=data,
            order=self.order,
            rows_size=1,
            cols_size=12,
            padding="0,0,0,0",
        )
        self.order += len(data)

    def plotGenres(self) -> None:
        """
        Plots a bar chart for games releases by genre.

        Returns:
        - None
        """
        dfVG_Sales = self.dfs["Video_Games_Sales_as_at_22_Dec_2016"]
        genresCount = (
            dfVG_Sales[dfVG_Sales.Year_of_Release < 2017]
            .Genre.groupby(dfVG_Sales.Genre)
            .count()
        )
        data = [
            {"Genre": index, "Games Released": row}
            for index, row in genresCount.items()
        ]
        self.shimoku.plt.bar(
            data=data,
            x="Genre",
            order=self.order,
            rows_size=2,
            cols_size=10,
            padding="0,1,0,1",
            x_axis_name="Genres",
            y_axis_name="Video Games Releases",
            title="Games Releases by Genre",
        )
        self.order += 1
    def getTop3Data(self, column: str) -> None:
        """
        Gets data for the top 3 items in the specified column and sets up KPIs.

        Parameters:
        - column (str): The column for which top 3 data is to be obtained.

        Returns:
        - None
        """
        df = self.dfs["Video_Games_Sales_as_at_22_Dec_2016"]
        dftop3 = utils.getTopN(df, column, 3)
        top1 = str(dftop3.iloc[0][column])
        top2 = str(dftop3.iloc[1][column])
        top3 = str(dftop3.iloc[2][column])

        top1FirstRelease, top1LastRelease = utils.firstLastRelease(df, column, top1)
        top2FirstRelease, top2LastRelease = utils.firstLastRelease(df, column, top2)
        top3FirstRelease, top3LastRelease = utils.firstLastRelease(df, column, top3)

        main_kpis = [
            {
                "title": f"Top 1 {column}",
                "description": f"{column} first place in sales",
                "value": top1,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top1} First Release",
                "description": f"{column} first year",
                "value": top1FirstRelease,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top1} Last Release",
                "description": f"{column} first year",
                "value": top1LastRelease,
                "color": "success",
                "align": "center",
            },
        ]

        self.df_app = {"main_kpis": pd.DataFrame(main_kpis)}

        main_kpis2 = [
            {
                "title": f"Top 2 {column}",
                "description": f"{column} second place in sales",
                "value": top2,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top2} First Release",
                "description": f"{column} first year",
                "value": top2FirstRelease,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top2} Last Release",
                "description": f"{column} last year",
                "value": top2LastRelease,
                "color": "success",
                "align": "center",
            },
        ]

        self.df_app2 = {"main_kpis2": pd.DataFrame(main_kpis2)}

        main_kpis3 = [
            {
                "title": f"Top 3 {column}",
                "description": f"{column} third place in sales",
                "value": top3,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top3} First Release",
                "description": f"{column} first year",
                "value": top3FirstRelease,
                "color": "success",
                "align": "center",
            },
            {
                "title": f"{top3} Last Release",
                "description": f"{column} last year",
                "value": top3LastRelease,
                "color": "success",
                "align": "center",
            },
        ]

        self.df_app3 = {"main_kpis3": pd.DataFrame(main_kpis3)}

    def plotTop3(self) -> None:
        """
        Plots KPIs for the top 3 items in the 'Genre' and 'Platform' columns.

        Returns:
        - None
        """
        from paths.top3 import Top3

        self.getTop3Data('Genre')

        T3G = Top3(self)
        T3G.plot()

        self.getTop3Data('Platform')

        T3G.df_app = self.df_app
        T3G.df_app2 = self.df_app2
        T3G.df_app3 = self.df_app3

        T3G.plot()


        
