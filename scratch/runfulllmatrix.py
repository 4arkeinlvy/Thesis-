from pathlib import Path
from itertools import product

CHECKPOINT_DIR = MODELDIR / 'checkpoints'

results = []
combos = list(product(img_embs.keys(), txt_embs.keys()))
print(f'Total combos: {len(combos)}')

for i, (img, txt) in enumerate(combos):
    print(f'\n[{i+1}/{len(combos)}] {img} + {txt}')
    try:
        r = train_and_eval(img, txt, iterations=1000, depth=6, save_dir=CHECKPOINT_DIR)
        results.append(r)
        print(f"  CatBoost: acc={r['acc_catboost']:.4f}, f1={r['f1_catboost']:.4f}")
        print(f"  +PGS:     acc={r['acc_pgs']:.4f},     f1={r['f1_pgs']:.4f}   Δacc={r['delta_acc']:+.4f}")

        # save CSV per iterasi — kalau crash di tengah, progress aman
        pd.DataFrame(results).to_csv(MODELDIR / 'matrix_results.csv', index=False)
    except Exception as e:
        print(f'  ERROR: {e}')
        results.append({'image': img, 'text': txt, 'error': str(e)})

results_df = pd.DataFrame(results)
if 'acc_pgs' in results_df.columns:
    results_df = results_df.sort_values('acc_pgs', ascending=False)
results_df.to_csv(MODELDIR / 'matrix_results.csv', index=False)

print('\n=== Top 3 ===')
cols = [c for c in ['image', 'text', 'acc_catboost', 'acc_pgs', 'delta_acc'] if c in results_df.columns]
print(results_df.head(3)[cols])
results_df
