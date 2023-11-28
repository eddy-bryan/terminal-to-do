To get started, set up a Google Sheets template using the 'template.xlsx' file provided. Download the file to your computer, from your Google Sheets account, create a new spreadsheet and select file > import and drag over the downloaded file into the area highlighted to create your own task list. (ensure that you rename the file to 'terminal_to_do' or change the code 'SHEET = GSPREAD_CLIENT.open('terminal_to_do')' appropriately.)

nagivate to google cloud
select a project > new project > name project
select project > APIs and services > library
search: google drive API 'enable'
create credentials > copy Code Institute guide
import file, rename to creds.json
copy email without quotes from creds.json file and share your google sheet file to the email address
you are set up





# Setting Up Google Sheets Template for Terminal To Do

### 1. Download Template File:

- Download the provided 'template.xlsx' file to your computer.

### 2. Create a New Spreadsheet on Google Sheets:

- Open your Google Sheets account.
- Create a new spreadsheet.
- Select File > Import and drag the downloaded 'template.xlsx' file into the highlighted area.
- This will create your personalized task list.

### 3. Rename the File:

- Ensure that you rename the file to 'terminal_to_do' or modify the following code accordingly:

    `SHEET = GSPREAD_CLIENT.open('terminal_to_do')`

# Setting Up Google Cloud and API Credentials

### 1. Navigate to Google Cloud Console:

- Visit the [Google Cloud Console](https://console.cloud.google.com/).

### 2. Create a New Project:

- Select Project > New Project.
- Name your project.

### 3. Enable Google Drive API:

- In the project dashboard, select APIs and Services > Library.
- Search for 'Google Drive API' and enable it.

### 4. Create Credentials:

- Navigate to APIs and Services > Credentials.
- Click on Create Credentials.
- Follow the provided Code Institute guide for creating credentials (below).

### 5. Import Credentials File:

- Import the credentials file generated during the credential creation process.
- Rename the file to 'creds.json'.

### 6. Share Google Sheet with API Email:

- Copy the email (without quotes) from the 'creds.json' file.
- Share your Google Sheet file with this email address.

### 7. You are now set up to use Terminal To Do with Google Sheets integration.

# Code Institute's Guide:

## Steps to get your credentials file for users with the "new" form UI:

1. From the "Which API are you using?" dropdown menu, choose Google Drive API

2. For the "What data will you be accessing?" question, select Application Data

3. For the "Are you planning to use this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions?" question, select No, I'm not using them

4. Click Next

5. Enter a Service Account name, you can call it anything you like - I will call mine "LoveSandwiches" - then click Create

6. In the Role Dropdown box choose Basic > Editor then press Continue

7. These options can be left blank, click Done

8. On the next page, click on the Service Account that has been created

9. On the next page, click on the Keys tab

10. Click on the Add Key dropdown and select Create New Key

11. Select JSON and then click Create. This will trigger the json file with your API credentials in it to download to your machine.