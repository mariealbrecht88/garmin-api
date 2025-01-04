# Introduction 

This API is used to get the the data from Garmin Connect.

This code is written using FastAPI

# About

This code is ported as fastAPI from [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)

# API Endpoints

## Get Full Name

- **Endpoint**: `/get_full_name`
- **Method**: `GET`
- **Description**: Fetches the full name of the user.

## Get Unit System

- **Endpoint**: `/get_unit_system`
- **Method**: `GET`
- **Description**: Fetches the unit system of the user.

## Get Activity Data

- **Endpoint**: `/get_activity_data`
- **Method**: `GET`
- **Description**: Fetches the activity data for a specific date.
- **Parameters**:
  - `date` (optional): The date for which to fetch the activity data. Defaults to today's date.

## Get Body Composition

- **Endpoint**: `/get_body_composition`
- **Method**: `GET`
- **Description**: Fetches the body composition data for a specific date.
- **Parameters**:
  - `date` (optional): The date for which to fetch the body composition data. Defaults to today's date.

## Get Steps Data

- **Endpoint**: `/get_steps_data`
- **Method**: `GET`
- **Description**: Fetches the steps data for a specific date.
- **Parameters**:
  - `date` (optional): The date for which to fetch the steps data. Defaults to today's date.

## Get Heart Rate Data

- **Endpoint**: `/get_heart_rate_data`
- **Method**: `GET`
- **Description**: Fetches the heart rate data for a specific date.
- **Parameters**:
  - `date` (optional): The date for which to fetch the heart rate data. Defaults to today's date.

## Get Training Readiness

- **Endpoint**: `/get_training_readiness`
- **Method**: `GET`
- **Description**: Fetches the training readiness data for a specific date.
- **Parameters**:
  - `date` (optional): The date for which to fetch the training readiness data. Defaults to today's date.

## Get Activities

- **Endpoint**: `/get_activities`
- **Method**: `GET`
- **Description**: Fetches the activities data.
- **Parameters**:
  - `start` (optional): The starting index for fetching activities. Defaults to 0.
  - `limit` (optional): The number of activities to fetch. Defaults to 100.

## Get Last Activity

- **Endpoint**: `/get_last_activity`
- **Method**: `GET`
- **Description**: Fetches the last activity data.

## Get Previous Day Steps

- **Endpoint**: `/get_previous_day_steps`
- **Method**: `GET`
- **Description**: Fetches the steps data for the previous day.
- **Parameters**:
  - `date` (optional): The date for which to fetch the steps data. Defaults to the previous day.
