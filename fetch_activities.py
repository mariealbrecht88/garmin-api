#!/usr/bin/env python3
"""
Script to fetch Garmin Connect activities from January 1, 2025 onward.
Saves the activities to a JSON file.
"""

import os
import json
import logging
from datetime import datetime, date
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from garth.exc import GarthHTTPError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def login_to_garmin():
    """
    Login to Garmin Connect.
    First tries to use saved tokens, then falls back to email/password.
    """
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    TOKENSTORE = os.getenv("GARMINTOKENS") or os.path.expanduser("~/.garminconnect")
    
    garmin = Garmin()
    
    # Try to login with saved tokens
    try:
        logger.info("Attempting to login with saved tokens...")
        garmin.login(TOKENSTORE)
        logger.info("Successfully logged in with saved tokens")
        return garmin
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        logger.info("Saved tokens not found or expired, logging in with credentials...")
        
        if not EMAIL or not PASSWORD:
            raise ValueError(
                "Please set EMAIL and PASSWORD environment variables:\n"
                "export EMAIL='your-email@example.com'\n"
                "export PASSWORD='your-password'"
            )
        
        try:
            garmin = Garmin(email=EMAIL, password=PASSWORD, is_cn=False)
            garmin.login()
            # Save tokens for future use
            garmin.garth.dump(TOKENSTORE)
            logger.info("Successfully logged in and saved tokens")
            return garmin
        except (GarthHTTPError, GarminConnectAuthenticationError, GarminConnectConnectionError) as err:
            logger.error(f"Authentication failed: {err}")
            raise


def fetch_activities(garmin, start_date, end_date=None):
    """
    Fetch all activities between start_date and end_date.
    
    Args:
        garmin: Authenticated Garmin instance
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD' (defaults to today)
    
    Returns:
        List of activities
    """
    if end_date is None:
        end_date = date.today().isoformat()
    
    logger.info(f"Fetching activities from {start_date} to {end_date}...")
    
    try:
        activities = garmin.get_activities_by_date(
            startdate=start_date,
            enddate=end_date,
            activitytype=None  # Get all activity types
        )
        logger.info(f"Successfully fetched {len(activities)} activities")
        return activities
    except GarminConnectTooManyRequestsError:
        logger.error("Too many requests - rate limited by Garmin")
        raise
    except Exception as e:
        logger.error(f"Error fetching activities: {e}")
        raise


def save_activities_to_file(activities, filename="garmin_activities.json"):
    """
    Save activities to a JSON file.
    
    Args:
        activities: List of activity dictionaries
        filename: Output filename
    """
    output_path = os.path.join(os.getcwd(), filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(activities, f, indent=2, ensure_ascii=False)
        logger.info(f"Activities saved to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error saving activities to file: {e}")
        raise


def print_activity_summary(activities):
    """Print a summary of the fetched activities."""
    if not activities:
        logger.info("No activities found")
        return
    
    print("\n" + "="*80)
    print(f"ACTIVITY SUMMARY - Total: {len(activities)} activities")
    print("="*80)
    
    # Group by activity type
    activity_types = {}
    for activity in activities:
        activity_type = activity.get('activityType', {}).get('typeKey', 'unknown')
        if activity_type not in activity_types:
            activity_types[activity_type] = 0
        activity_types[activity_type] += 1
    
    print("\nActivities by Type:")
    for activity_type, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {activity_type}: {count}")
    
    print("\nRecent Activities (last 10):")
    print("-"*80)
    for activity in activities[:10]:
        activity_name = activity.get('activityName', 'Unnamed')
        activity_type = activity.get('activityType', {}).get('typeKey', 'unknown')
        start_time = activity.get('startTimeLocal', 'Unknown time')
        distance = activity.get('distance', 0) / 1000  # Convert to km
        duration = activity.get('duration', 0) / 60  # Convert to minutes
        
        print(f"  {start_time[:10]} | {activity_name[:30]:30} | {activity_type:15} | {distance:.2f} km | {duration:.0f} min")
    
    print("="*80 + "\n")


def main():
    """Main function to fetch and save Garmin activities."""
    try:
        # Login to Garmin
        garmin = login_to_garmin()
        
        # Display user info
        full_name = garmin.get_full_name()
        logger.info(f"Logged in as: {full_name}")
        
        # Set date range
        start_date = "2025-01-01"
        end_date = date.today().isoformat()
        
        # Fetch activities
        activities = fetch_activities(garmin, start_date, end_date)
        
        # Print summary
        print_activity_summary(activities)
        
        # Set output directory (shared data folder)
        # This creates: ~/projects/personal/data/garmin/activities/
        home_dir = os.path.expanduser("~")
        output_dir = os.path.join(home_dir, "projects", "personal", "data", "garmin", "activities")
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to file
        output_filename = f"garmin_activities_{start_date}_to_{end_date}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(activities, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Activities saved to {output_path}")
        print(f"\n✅ Success! {len(activities)} activities saved to:\n   {output_path}")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())