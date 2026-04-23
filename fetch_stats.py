import json
import os
from datetime import datetime, timezone
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric

service_account_info = json.loads(os.environ["GA_SERVICE_ACCOUNT"])
property_id = os.environ["GA_PROPERTY_ID"]

client = BetaAnalyticsDataClient.from_service_account_info(service_account_info)

request = RunReportRequest(
    property=f"properties/{property_id}",
    date_ranges=[DateRange(start_date="2026-04-20", end_date="today")],
    metrics=[
        Metric(name="totalUsers"),
        Metric(name="screenPageViews"),
    ],
)

response = client.run_report(request)
row = response.rows[0].metric_values

stats = {
    "visitors": int(row[0].value),
    "pageviews": int(row[1].value),
    "updated": datetime.now(timezone.utc).isoformat(),
}

with open("stats.json", "w") as f:
    json.dump(stats, f)

print(f"Stats updated: {stats}")
