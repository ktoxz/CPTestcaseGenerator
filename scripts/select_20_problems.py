import pyarrow.parquet as pq
from collections import Counter
import pandas as pd

table = pq.read_table('d:/KLTN/Final_TestcaseGenerator/data/cache_hf/0000.parquet', columns=['problem_id', 'contestId', 'problem_index', 'verdict', 'programmingLanguage'])
df = table.to_pandas()

# Filter for C++ submissions
df_cpp = df[df['programmingLanguage'].str.contains('C\\+\\+', na=False)]

p_stats = []
for pid, grp in df_cpp.groupby('problem_id'):
    c_id, p_idx = pid.split('/')
    v_counts = Counter(grp['verdict'])
    ok = v_counts.get('OK', 0)
    wa = v_counts.get('WRONG_ANSWER', 0)
    if ok >= 15 and wa >= 10:
        p_stats.append({
            'problem_id': pid,
            'contestId': c_id,
            'problem_index': p_idx,
            'ok': ok,
            'wa': wa,
            'total': len(grp)
        })

p_stats.sort(key=lambda x: x['total'], reverse=True)
print(f"Total problems meeting criteria (>=15 AC, >=10 WA in C++): {len(p_stats)}")

# Select top 20
selected = p_stats[:20]
for idx, s in enumerate(selected, 1):
    cf_slug = f"cf{s['contestId']}{s['problem_index'].lower()}"
    print(f"{idx:2d}. {cf_slug:10} (CF {s['problem_id']:8}): AC={s['ok']:4}, WA={s['wa']:4}")
