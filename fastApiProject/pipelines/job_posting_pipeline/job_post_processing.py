import requests

api_url = "https://utsc-utoronto-csm.symplicity.com/api/public/v1/jobs"
token = "AW+EbaUTXP6MZerfald5k1Kycit/okaadmfJ07/05+YIQrJ/SnWasBgV9uInuybgOjjxuu9PGwsc6g1jdgGWo3Ru7aOzUa5MIFADpEvFw5+9Ic7tO7krBUw8FY82u5SznBbT4y1uoGybJSqICrsuqg=="
headers = {
    "Authorization": f"Token {token}"
}

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    job_data = response.json()
    print(job_data)
else:
    print(f"Error: Unable to fetch job data. Status code: {response.status_code}")
