# Rice VPAA SDK

Internal SDK for accessing the Rice VPAA API. Requires an API key.

## Install
```bash
pip install rice-vpaa
```

## Documentation

Full Swagger API documentation is available [here](https://vpaa-api-server-stnkl.ondigitalocean.app/docs).

## Usage
```python
from rice_vpaa import VPAAClient
client = VPAAClient(api_key="your-api-key")
```

## Get Faculty
```python
faculty = client.get_faculty(
    unit_ids=[123],
    tenure_statuses=["TTT"],
    employment_statuses=["Full Time"]
)
```

## Get Divisions
```python
divisions = client.get_divisions(departments_only=True)
```

## Get Open Positions
```python
positions = client.get_open_positions()
```
