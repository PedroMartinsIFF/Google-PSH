```markdown
# Google Service Health Event Script

This repository contains a Python script to interact with the Google Service Health API. The script can list all events for a specified project and provide detailed information for a specific event.

## Prerequisites

- Python 3.x
- `requests` library
- `google-auth` library
- `dateutil` library

You can install the required libraries using pip:

```bash
pip3 install requests google-auth python-dateutil
```

## Usage

### Listing Events

To list all events for a specified project, use the following command:

```bash
python3 get_psh.py event_list <project_id>
```

### Fetching Event Details

To fetch detailed information for a specific event, use the following command:

```bash
python3 get_psh.py event_detail <project_id> <event_id>
```

## Script Details

### `get_psh.py`

This script interacts with the Google Service Health API to list events and fetch event details.

#### Command-Line Arguments

- `opcao`: The operation to perform (`event_list` or `event_detail`).
- `project_id`: The Google Cloud project ID.
- `event_id`: The ID of the event to fetch details for (only required for `event_detail`).

#### Event Listing (`event_list`)

- Fetches a list of events for the specified project.
- Extracts and prints event details such as `EVENTID` and `TITLE`.

#### Event Details (`event_detail`)

- Fetches detailed information for a specific event using its `EVENTID`.
- Extracts and prints detailed event information including `TITLE`, `CATEGORY`, `STATE`, `SERVICES`, and timestamps (`STARTTIME`, `ENDTIME`, `UPDATETIME`, `NEXTUPDATETIME`).

## Example

### Listing Events

```bash
python3 get_psh.py event_list my_project_id
```

### Fetching Event Details

```bash
python3 get_psh.py event_detail my_project_id my_event_id
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

