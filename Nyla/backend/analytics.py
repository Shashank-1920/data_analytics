import re
import pandas as pd
import math
from datetime import timedelta


def _find_date_column(df):
    """Return the best candidate column name for dates, or None."""
    try:
        datetime_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    except Exception:
        datetime_cols = []
    if datetime_cols:
        return datetime_cols[0]

    patterns = [r'date', r'_at$', r'timestamp', r'time', r'deliver', r'order', r'created']
    for c in df.columns:
        lname = c.lower()
        if any(re.search(pat, lname) for pat in patterns):
            return c
    return None


def _find_customer_column(df):
    """Return the best candidate column name for customer identifier, or None."""
    candidates = []
    for c in df.columns:
        lname = c.lower()
        # prefer explicit id columns
        if 'customer' in lname or 'client' in lname or lname.startswith('cust') or 'account' in lname:
            candidates.append(c)

    if candidates:
        for c in candidates:
            if 'id' in c.lower():
                return c
        return candidates[0]

    id_cols = [c for c in df.columns if 'id' in c.lower()]
    return id_cols[0] if id_cols else None


def _find_customer_name_column(df, customer_col=None):
    """Return a candidate column that likely contains the customer name."""
    # prefer columns containing 'name' but not 'id'
    for c in df.columns:
        lname = c.lower()
        if 'name' in lname and 'id' not in lname:
            return c

    # fallback: common patterns
    name_patterns = ['customer name', 'customer_name', 'account name', 'account_name', 'client_name']
    for pat in name_patterns:
        for c in df.columns:
            if pat in c.lower() and 'id' not in c.lower():
                return c

    # if nothing obvious, try string columns (not the customer id)
    string_cols = [c for c in df.columns if df[c].dtype == object]
    for c in string_cols:
        if c.lower() != (customer_col or '').lower():
            if df[c].notna().any():
                return c
    return None


def perform_analytics(connection, table_name):
    """Perform customer-wise analytics and return JSON-serializable records."""
    query = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(query, connection)

    if df.empty:
        return []

    date_col = _find_date_column(df)
    customer_col = _find_customer_column(df)
    name_col = _find_customer_name_column(df, customer_col)

    if not date_col or not customer_col:
        found = {
            'columns': list(df.columns),
            'detected_date_column': date_col,
            'detected_customer_column': customer_col,
        }
        raise ValueError(f"Table must contain at least one date and one customer identifier column. Detection: {found}")

    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    if df[date_col].isna().all():
        raise ValueError(f"Detected date column '{date_col}' could not be parsed as dates.")

    df = df.sort_values(by=[customer_col, date_col])

    # compute basic order stats per customer
    customer_orders = df.groupby(customer_col).agg({
        date_col: ['count', 'min', 'max']
    }).reset_index()
    customer_orders.columns = ['customer_id', 'total_orders', 'first_order_date', 'last_order_date']

    # attach customer name if available
    if name_col and name_col in df.columns:
        names = (
            df.groupby(customer_col)[name_col]
            .apply(lambda s: s.dropna().astype(str).iloc[0] if not s.dropna().empty else None)
            .reset_index()
        )
        # Normalize the name mapping to use 'customer_id' as the join key so
        # we don't accidentally drop the primary id column when merging.
        names = names.rename(columns={customer_col: 'customer_id', name_col: 'customer_name'})
        customer_orders = customer_orders.merge(names, on='customer_id', how='left')
    else:
        customer_orders['customer_name'] = None

    # compute average gaps
    order_gaps = []
    for customer_id, group in df.groupby(customer_col):
        dates = group[date_col].sort_values().tolist()
        if len(dates) > 1:
            gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
            avg_gap = float(sum(gaps)) / len(gaps)
        else:
            avg_gap = float('nan')
        order_gaps.append({'customer_id': customer_id, 'avg_order_gap': avg_gap})

    gaps_df = pd.DataFrame(order_gaps)
    results = customer_orders.merge(gaps_df, left_on='customer_id', right_on='customer_id', how='left')

    def _predict_next(row):
        try:
            gap = row.get('avg_order_gap', None)
            if gap is None or (isinstance(gap, float) and math.isnan(gap)):
                return None
            gap = float(gap)
            if gap > 0:
                last = row['last_order_date']
                if pd.notna(last):
                    return last + timedelta(days=round(gap))
        except Exception:
            pass
        return None

    results['predicted_next_order_date'] = results.apply(_predict_next, axis=1)

    def classify_customer(gap):
        try:
            if gap is None or (isinstance(gap, float) and math.isnan(gap)):
                return 'Unknown'
            gap = float(gap)
        except Exception:
            return 'Unknown'
        if gap <= 0:
            return 'Unknown'
        if gap < 7:
            return 'Frequent'
        if gap < 30:
            return 'Moderate'
        return 'Infrequent'

    results['customer_classification'] = results['avg_order_gap'].apply(classify_customer)

    # convert dates to ISO strings or None
    def _dt_to_str(v):
        if pd.isna(v):
            return None
        try:
            return pd.Timestamp(v).isoformat()
        except Exception:
            return str(v)

    results['first_order_date'] = results['first_order_date'].apply(_dt_to_str)
    results['last_order_date'] = results['last_order_date'].apply(_dt_to_str)
    results['predicted_next_order_date'] = results['predicted_next_order_date'].apply(_dt_to_str)

    # normalize avg_order_gap: round or None
    def _safe_round(x):
        try:
            if x is None or (isinstance(x, float) and math.isnan(x)):
                return None
            return round(float(x), 2)
        except Exception:
            return None

    results['avg_order_gap'] = results['avg_order_gap'].apply(_safe_round)

    records = results.to_dict('records')

    # final cleanup
    for record in records:
        for k, v in list(record.items()):
            if isinstance(v, float) and math.isnan(v):
                record[k] = None

    return records
