# Streaming Video Subscriptions (MavenFlix)

Subscription records for **MavenFlix**, a fictitious video streaming platform.

This dataset contains information for ~2,900 subscribers covering **September 2022 through September 2023**. Each row represents an individual customer subscription, including subscription cost, created/canceled dates, billing interval, and payment status.

## Dataset Contents

- **subscription records** (one row per customer subscription)
- Time period:
  - **2022-09** to **2023-09** (inclusive)

Typical fields include (names may vary depending on the CSV you downloaded):
- `customer_id` / `subscriber_id`
- `created_date` (subscription start date)
- `canceled_date` (subscription cancellation date; often null for active subs)
- `subscription_cost`
- `interval` (e.g., monthly, annual)
- `payment_status` (e.g., paid, past_due, failed)
- `is_active` (derived or provided)

## Recommended Analysis

### 1) How have MavenFlix subscriptions trended over time?
Suggested metrics:
- New subscriptions per month (count of `created_date`)
- Cancellations per month (count of `canceled_date`)
- Active subscribers over time (created <= date AND (canceled is null OR canceled > date))

Common outputs:
- Monthly line chart of new subs vs cancellations
- Monthly active subscriber trend

### 2) What percentage of customers have subscribed for 5 months or more?
Approach:
- Compute `subscription_length_days = (canceled_date or period_end) - created_date`
- Convert to months (e.g., `days / 30.44`) or count month boundaries
- Calculate:
  - `pct_5_months_plus = customers_with_length >= 5 months / total_customers`

Notes:
- For active subscriptions (no `canceled_date`), use the dataset end date (e.g., `2023-09-30`) as the end of the observation window.

### 3) What month has the highest subscriber retention, the lowest retention?
Recommended method (cohort retention):
- Define a cohort as the month of `created_date` (e.g., `2022-09`)
- For each cohort, compute how many subscribers are still active in month 1, 2, 3, ...
- Retention for a cohort-month = retained users / cohort size
- Identify:
  - Highest retention cohort (e.g., best month-1 or month-5 retention)
  - Lowest retention cohort

## Assumptions / Data Quality Notes

- `canceled_date` may be missing for active subscribers.
- Payment status may impact “active” definition. Decide whether:
  - “active” means not canceled, OR
  - “active & paying” means not canceled AND payment status is good.
- Some customers may appear more than once if they churn and resubscribe (depends on source). If so, decide whether to:
  - treat each row as a separate subscription, OR
  - aggregate to one record per customer.

## Getting Started

### Option A: Analyze in Python (pandas)
1. Create a virtual environment
2. Install dependencies:
   - `pandas`
   - `numpy`
   - (optional) `matplotlib` / `seaborn` for charts

3. Load the CSV and parse dates:
- Parse `created_date` and `canceled_date`
- Fill `is_active` where `canceled_date` is null (if needed)

### Option B: Analyze in SQL
1. Load the CSV into your database (Postgres, BigQuery, etc.)
2. Create derived columns:
- `created_month`
- `canceled_month`
- `subscription_duration`

## Example KPIs to Report

- Total subscribers
- New subscribers per month
- Cancellations per month
- Active subscribers at month-end
- Churn rate (monthly) = cancellations / starting active subscribers
- Retention by cohort (month 1, month 2, month 3, ...)

## License / Disclaimer

This dataset represents a **fictitious** product (MavenFlix). Use for analytics practice, portfolio projects, and learning.