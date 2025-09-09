
import urllib.request
import ssl
from bs4 import BeautifulSoup
import pandas as pd # Optional: to structure the data
pd.options.mode.copy_on_write = True

macos_ver = {'sierra': 16, 'high_sierra': 17,
             'mojave': 18, 'catalina': 19}

url = 'https://en.wikipedia.org/wiki/Darwin_(operating_system)'
headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
try:
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, context=ssl.create_default_context(ssl.Purpose.SERVER_AUTH))
    # Note: urllib doesn't have raise_for_status, so we'll handle it manually
    if response.getcode() != 200:
        raise Exception(f"HTTP Error: {response.getcode()}")
    soup = BeautifulSoup(response.read(), 'html.parser')

    # Find the table - this requires inspecting the page source
    # Look for attributes like id, class, or surrounding elements
    # For the "Darwin 20 onwards" section, you might need to find the heading first
    heading = soup.find(id="Darwin_20_onwards")
    if heading:
        # Find the table *after* this heading
        table = heading.find_next("table", {"class": "wikitable"}) # Example: find next wikitable
    else:
        # Fallback: Find based on table properties if heading isn't found easily
        # This might require more specific inspection of the page HTML
        table = soup.find("table", {"class": "wikitable"}) # Adjust selector as needed

    if table:
        # Extract data (example using pandas for convenience)
        darwin_table_df = pd.read_html(str(table))[0]
        selected_columns = darwin_table_df[['Version', 'Corresponding releases']]
        extracted_names = selected_columns['Corresponding releases'].str.extract(
            r"macOS\s+(.*?)iOS", expand=False
        )
        processed_names = extracted_names.fillna("").str.strip().str.lower().str.replace(' ', '_')
        selected_columns['macOS_name_processed'] = processed_names
        major_versions_series = pd.to_numeric(
            selected_columns['Version'].str.split('.').str[0], errors='coerce'
        )
        selected_columns['major_version'] = major_versions_series
        valid_rows_df = selected_columns[
            (selected_columns['macOS_name_processed'] != '') &
            (selected_columns['major_version'].notna())
        ].copy()
        valid_rows_df['major_version'] = valid_rows_df['major_version'].astype(int)
        unique_mapping_df = valid_rows_df.drop_duplicates(
            subset='macOS_name_processed',
            keep='first'
        )
        macos_version_dict = unique_mapping_df.set_index('macOS_name_processed')['major_version'].to_dict()
        macos_ver = {**macos_ver, **macos_version_dict}

        print(macos_ver)


    else:
        print("Could not find the target table.")

except ImportError:
    print("Please install requests and beautifulsoup4 (pip install requests beautifulsoup4)")
except urllib.error.URLError as e:
    print(f"Error fetching URL: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
