# Garmin Activities Fetcher

This script fetches all your Garmin Connect activities from January 1, 2025 onward and saves them to a JSON file.

## Setup

### 1. Install Dependencies

Make sure you're in the garmin-api folder and install the required packages:

```bash
uv pip install -r requirements.txt
```

### 2. Set Your Credentials

Set your Garmin Connect credentials as environment variables:

```bash
export EMAIL="your-email@garmin.com"
export PASSWORD="your-password"
```

**Note:** After the first login, your authentication tokens will be saved to `~/.garminconnect` and you won't need to provide credentials again.

## Usage

### Basic Usage

Simply run the script:

```bash
python fetch_activities.py
```

This will:
1. Login to Garmin Connect
2. Fetch all activities from January 1, 2025 to today
3. Display a summary in the terminal
4. Save all activities to a JSON file named `garmin_activities_2025-01-01_to_YYYY-MM-DD.json`

### Example Output

```
2025-01-17 10:30:15 - INFO - Attempting to login with saved tokens...
2025-01-17 10:30:16 - INFO - Successfully logged in with saved tokens
2025-01-17 10:30:16 - INFO - Logged in as: John Doe
2025-01-17 10:30:16 - INFO - Fetching activities from 2025-01-01 to 2025-01-17...
2025-01-17 10:30:18 - INFO - Successfully fetched 25 activities

================================================================================
ACTIVITY SUMMARY - Total: 25 activities
================================================================================

Activities by Type:
  running: 12
  cycling: 8
  strength_training: 5

Recent Activities (last 10):
--------------------------------------------------------------------------------
  2025-01-17 | Morning Run                    | running         | 5.23 km | 28 min
  2025-01-16 | Evening Bike Ride              | cycling         | 15.40 km | 45 min
  ...
================================================================================

2025-01-17 10:30:18 - INFO - Activities saved to /path/to/garmin_activities_2025-01-01_to_2025-01-17.json

✅ Success! 25 activities saved to garmin_activities_2025-01-01_to_2025-01-17.json
```

## Output File Format

The script saves activities as a JSON array. Each activity contains detailed information including:

- Activity name and type
- Start time and duration
- Distance, pace, and speed
- Heart rate data
- Calories burned
- GPS coordinates (if available)
- And much more...

Example structure:

```json
[
  {
    "activityId": 12345678901,
    "activityName": "Morning Run",
    "activityType": {
      "typeKey": "running",
      "typeId": 1
    },
    "startTimeLocal": "2025-01-17 07:30:00",
    "distance": 5234.5,
    "duration": 1680.0,
    "averageHR": 145,
    "maxHR": 172,
    "calories": 420,
    ...
  }
]
```

## Customization

You can modify the script to:

### Change the date range

Edit line 130 in the script:

```python
start_date = "2024-01-01"  # Change to your desired start date
```

### Filter by activity type

Modify the `fetch_activities` call on line 137:

```python
activities = fetch_activities(
    garmin, 
    start_date, 
    end_date,
    activitytype="running"  # Options: running, cycling, swimming, etc.
)
```

And update the function signature on line 45:

```python
def fetch_activities(garmin, start_date, end_date=None, activitytype=None):
    # ...
    activities = garmin.get_activities_by_date(
        startdate=start_date,
        enddate=end_date,
        activitytype=activitytype
    )
```

## Troubleshooting

### Authentication Failed

Make sure your EMAIL and PASSWORD environment variables are set correctly:

```bash
echo $EMAIL
echo $PASSWORD
```

### Rate Limiting

If you get a "Too many requests" error, wait a few minutes before trying again. Garmin limits the number of API requests.

### No Activities Found

- Check that you have activities in your Garmin Connect account for the specified date range
- Verify the date format is 'YYYY-MM-DD'

## File Placement

**Recommended:** Place `fetch_activities.py` in the same folder as your garmin-api project. This way it can use the same dependencies.

Your folder structure should look like:
```
garmin-api/
├── garminconnect/
├── main.py
├── app.yaml
├── README.md
└── fetch_activities.py  ← Your new script
```

## Next Steps

Once you have your activities in JSON format, you can:

1. **Analyze your data** with pandas:
   ```python
   import pandas as pd
   import json
   
   with open('garmin_activities_2025-01-01_to_2025-01-17.json') as f:
       activities = json.load(f)
   
   df = pd.DataFrame(activities)
   print(df[['activityName', 'startTimeLocal', 'distance', 'duration']].head())
   ```

2. **Create visualizations** of your training data
3. **Export to CSV** for use in spreadsheets
4. **Build a dashboard** to track your progress

Let me know if you need help with any of these!