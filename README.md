# Google Sheets Integration Solution via AWS Lambda

This solution enables integration between an application and **Google Sheets** using the **Google Sheets API**. It allows users to retrieve all records from a specified Google Sheets document through an AWS Lambda function and API Gateway.

## Features

- **Easy Access to Data:** Fetches all records from a specified Google Sheets document.
- **Secure Authentication:** Uses service account credentials for secure access to Google Sheets.
- **Flexible Input:** Accepts parameters to specify the Google Sheets document and the worksheet.

## How the Solution Works

1. **API Request:**
   - Users send a GET request to the Lambda function's endpoint.
   - The request must include the `spreadsheet_id` and the `worksheet_name` as query parameters.

2. **Access Google Sheets:**
   - The Lambda function uses the Google Sheets API to authenticate using service account credentials.
   - It retrieves the specified worksheet's data from the Google Sheets document.

3. **Return Data:**
   - The function returns all records from the worksheet as a JSON response.

## AWS Implementation with Terraform

This solution has been fully implemented on AWS using **Terraform**. Below are the details on how to configure and use Terraform to provision the necessary resources.

### 1. Prerequisites
- Install [Terraform](https://www.terraform.io/downloads.html).
- Install [AWS CLI](https://aws.amazon.com/cli/).
- Configure AWS credentials in your local environment.

### 2. Running Terraform
- First you have to zip the lambda function and zip the requirements in google sheets layer folder.
- Then you have to put it in the deployments folder, inside terraform folder.

- To provision the resources, run the following commands in the command line:

```bash
terraform init
terraform apply
```

### 3. Obtain the API Gateway Link
After the `terraform apply` command, Terraform will provide the defined outputs, including the link to the API Gateway. Use this link to send requests to the Lambda function.

## Google Cloud Configuration for Sheets API

To ensure proper functionality of the Google Sheets API, follow the steps below to configure Google Cloud:

### 1. Create a Google Cloud Account
- If you do not have a Google Cloud account, [sign up here](https://cloud.google.com/).

### 2. Enable the Google Sheets API
- Access the **Google Cloud Console** ([cloud.google.com](https://cloud.google.com)).
- In the APIs menu, search for **Google Sheets API** and enable it for your project.

### 3. Create Service Account Credentials
- In the **Google Cloud Console**, go to **APIs & Services** > **Credentials**.
- Click on **Create Credentials** and select **Service Account**.
- Fill in the required details and create the service account.
- Once created, click on the service account, then navigate to the **Keys** tab and select **Add Key** > **JSON**.
- Download the generated JSON key file, which contains your service account credentials.

### 4. Store Credentials
- Place the downloaded JSON credentials file in the folder of the Lambda function that will use it. With the name `client_secret.json`.

### 5. Share Google Sheets with Service Account
- Open the Google Sheets document you want to access.
- Click on the **Share** button and add the service account email (client_email) (found in the JSON file) with at least **Viewer** access.

## Lambda Function Endpoint

### `POST /get_sheets_all_records`

#### Body:
- `spreadsheet_id` (str): The ID of the Google Sheets document.
- `worksheet_name` (**optional** str): The name of the worksheet from which to retrieve data. If not provided, the first worksheet will be used.

### Response

The response will be a JSON object containing all records from the specified worksheet.

## Conclusion

This solution provides a simple and effective way to integrate your application with Google Sheets, allowing for seamless data retrieval using AWS Lambda. Ensure you follow the Google Cloud configuration steps to enable smooth access to the Google Sheets API.
