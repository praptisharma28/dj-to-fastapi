import requests
import json
from datetime import datetime, timedelta

def fetch_call_logs(
    start_time,
    end_time,
    sr_key="67c13856-e912-4b10-ad3c-4726e8ccec6f",
    x_api_key="QdQa83awS05tyB0KAVATX7tvm3WuBXz16QEluhix",
    call_type=None,
    agent_number=None,
    knowlarity_number=None,
    business_call_type=None,
    customer_number=None,
    limit=None
):
    """
    Fetch call logs from Knowlarity API
    """
    
    # Use the URL that worked
    url = "https://kpi.knowlarity.com/Basic/v1/account/calllog"
    
    headers = {
        'channel': "Basic",
        'x-api-key': x_api_key,
        'authorization': sr_key,
        'content-type': "application/json",
        'cache-control': "no-cache",
    }
    
    # Build params dictionary instead of adding to headers
    params = {
        'start_time': start_time,
        'end_time': end_time
    }
    
    # Add optional parameters to the params if they are provided
    if call_type is not None:
        params['call_type'] = call_type
    if agent_number:
        params['agent_number'] = agent_number
    if knowlarity_number:
        params['knowlarity_number'] = knowlarity_number
    if business_call_type:
        params['business_call_type'] = business_call_type
    if customer_number:
        params['customer_number'] = customer_number
    if limit:
        params['limit'] = limit
    
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")
    
    # Make the request with parameters as query params
    response = requests.get(url, headers=headers, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        # Print the raw response for debugging
        print(f"Raw response: {response.text}")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def format_datetime(dt):
    """Format datetime object to required string format"""
    return dt.strftime("%Y-%m-%d %H:%M:%S+05:30")

# Example usage
if __name__ == "__main__":
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    start_time = format_datetime(yesterday)
    end_time = format_datetime(now)
    print(f"Fetching call logs from {start_time} to {end_time}...")
    logs = fetch_call_logs(
        start_time=start_time,
        end_time=end_time,
        sr_key="67c13856-e912-4b10-ad3c-4726e8ccec6f",
        x_api_key="QdQa83awS05tyB0KAVATX7tvm3WuBXz16QEluhix",
    )  
    if logs:
        print("\nResponse structure:")
        print(type(logs))
        print(json.dumps(logs, indent=4))
        call_logs = []
        if isinstance(logs, list):
            call_logs = logs
        elif isinstance(logs, dict):
            for key in ['data', 'calls', 'logs', 'call_logs', 'objects', 'results']:
                if key in logs and isinstance(logs[key], list):
                    call_logs = logs[key]
                    break
        
        if call_logs:
            print(f"\nRetrieved {len(call_logs)} call logs")
            print("\nSample Call Log Entry:")
            print(json.dumps(call_logs[0], indent=4))
        else:
            print("\nNo call logs found in the response, or format is unexpected.")
            print("You may need to modify the code to extract logs from the response structure.")
    else:
        print("Failed to retrieve call logs")