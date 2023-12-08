from os import getenv
from dotenv import load_dotenv
import shimoku_api_python as Shimoku
from dashboard import Dashboard


def main():
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve environment variables
    access_token = getenv("SHIMOKU_TOKEN")
    universe_id: str = getenv("UNIVERSE_ID")
    workspace_id: str = getenv("WORKSPACE_ID")

    # Initialize Shimoku client with the provided credentials

    s = Shimoku.Client(
        access_token=access_token,
        universe_id=universe_id,
    )

    # Set the workspace for Shimoku client
    s.set_workspace(uuid=workspace_id)

    # Create a Dashboard object using the Shimoku client
    dboard = Dashboard(s)

    # Set up and display the dashboard
    dboard.setDashboard()


if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
