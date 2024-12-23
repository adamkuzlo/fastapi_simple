import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1zVJZjqTlAbDUAXBisTlcs5XBoocm4lHen3t0hWt5SEA"
SAMPLE_RANGE_NAME = "predictions"  # Specify the entire sheet by its name

def main():
    """Shows basic usage of the Sheets API.
    Prints all values from the specified sheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        selected_columns_indices = [0, 1, 2, 3, 4, 5, 9, 10]
        filtered_data = [
            [row[i] if i < len(row) else "" for i in selected_columns_indices]
            for row in values
        ]

        # Print the filtered rows
        print("Filtered data (columns A, B, C, D, E, F, J, K):")
        for row in filtered_data:
            print(row)

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
