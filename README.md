# ReliefWeb MCP Server

Model Context Protocol (MCP) server for ReliefWeb humanitarian information API.

## Features

- **Reports**: Search humanitarian reports by country and theme
- **Disasters**: Track disasters and emergencies
- **Updates**: Get latest situation updates
- **Theme Filtering**: Food security, health, protection, etc.
- **Date Range Queries**: Historical and recent data

## Installation

```bash
pip install -e .
```

## Usage

### As MCP Server

```bash
python main.py
```

### In Cloudera Agent Studio

```json
{
  "name": "reliefweb-mcp-server",
  "type": "PYTHON",
  "args": ["--from", "git+https://github.com/mercycorps/reliefweb-mcp", "run-server"],
  "env_names": []
}
```

## Tools Available

### search_reports
Search humanitarian reports by country, keywords, and date range.

**Parameters:**
- `country` (str): Country name or ISO3 code
- `query` (str): Search keywords (optional)
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)
- `limit` (int): Max results (default 100)

### search_disasters
Search disasters and emergencies.

### search_updates
Get latest situation updates for a country.

## Example

```python
# Search food security reports for Sudan
result = await search_reports(
    country="SDN",
    query="food security",
    start_date="2024-01-01",
    end_date="2024-12-31",
    limit=100
)
```

## Data Source

ReliefWeb: https://reliefweb.int/
