r = train_and_eval(best_img, best_txt, iterations=1500, depth=6)

pgs_df = pd.DataFrame([
    {'model': 'CatBoost (no PGS)', 'accuracy': r['acc_catboost'], 'macro_f1': r['f1_catboost']},
    {'model': 'CatBoost + PGS',    'accuracy': r['acc_pgs'],      'macro_f1': r['f1_pgs']},
])
pgs_df.to_csv(MODELDIR / 'pgs_ablation.csv', index=False)
print('\n=== PGS Effect (Tabel 8 paper) ===')
print(pgs_df.to_string(index=False))
print(f"Δacc = {r['delta_acc']:+.4f}")
print(f"mean uncertainty = {r['mean_uncertainty']:.4f}")
pgs_df
