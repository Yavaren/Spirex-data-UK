from pytrends.request import TrendReq
import pandas as pd
import time
import os

# List of UK region geocodes
uk_region_geocodes = [
    'GB-ENG', 'GB-SCT', 'GB-WLS', 'GB-NIR', 'GB-LND', 'GB-BIR', 'GB-MAN', 'GB-LIV', 'GB-BST',
    'GB-GLA', 'GB-LEE', 'GB-SHE', 'GB-COV', 'GB-HUL', 'GB-BEL', 'GB-CAR', 'GB-EDH', 'GB-ABD',
    'GB-NEW', 'GB-NOT', 'GB-DER', 'GB-LEI', 'GB-SOU', 'GB-PLY', 'GB-SWA', 'GB-BRD', 'GB-MLN'
]

def fetch_trends_data(keywords, regions, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='en-GB', tz=0)
    all_data = pd.DataFrame()

    for region in regions:
        for keyword in keywords:
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=region, gprop='')
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                    interest_over_time_df['region'] = region
                    interest_over_time_df['keyword'] = keyword
                    all_data = pd.concat([all_data, interest_over_time_df])
                    print(f"Collected data for {keyword} in {region}")
                else:
                    print(f"No data for {keyword} in {region}.")
                time.sleep(60)  # Wait for 60 seconds to avoid hitting the rate limit
            except Exception as e:
                print(f"An error occurred for keyword {keyword} in {region}: {e}")
                time.sleep(60)  # Wait for 60 seconds before retrying with the next keyword

    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data_by_region.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop", "headphones", "tablet", "smartwatch",
    ]
    fetch_trends_data(kw_list, uk_region_geocodes, timeframe='2020-06-04 2024-06-04')
