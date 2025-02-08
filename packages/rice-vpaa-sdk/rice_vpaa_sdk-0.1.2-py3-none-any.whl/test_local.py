from rice_vpaa import VPAAClient
import os
from dotenv import load_dotenv

load_dotenv()


# Create client with test API key and local URL
client = VPAAClient(
    api_key=os.getenv("VPAA_API_KEY")
)


# Try getting divisions
print("\nTesting get_divisions:")
divisions = client.get_divisions(departments_only=True)
for division in divisions.divisions:
    print(f"{division.unit_name}:")
    for dept in division.departments:
        print(f"  - {dept.unit_name}")

# Try getting faculty
print("\nTesting get_faculty:")
faculty = client.get_faculty(
    unit_ids=[123],
    tenure_statuses=["TTT"]
)
print(f"Found {len(faculty.faculty)} faculty members")

# Try getting positions
print("\nTesting get_positions:")
positions = client.get_open_positions()
print(f"Found {len(positions.results)} open positions")