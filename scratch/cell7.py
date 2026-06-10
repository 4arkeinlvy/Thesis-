best = results_df.iloc[0]
best_img, best_txt = best['image'], best['text']
print(f'Best combo: {best_img} + {best_txt} (acc_pgs={best["acc_pgs"]:.4f})')

abl = []
for label, img, txt in [('image only', best_img, None),
                         ('text only',  None, best_txt),
                         ('fusion',     best_img, best_txt)]:
    print(f'\n--- {label} ---')
    r = train_and_eval(img, txt, iterations=1500, depth=6)
    r['config'] = label
    abl.append(r)
    print(f"  CatBoost: acc={r['acc_catboost']:.4f}, f1={r['f1_catboost']:.4f}")
    print(f"  +PGS:     acc={r['acc_pgs']:.4f},     f1={r['f1_pgs']:.4f}")

abl_df = pd.DataFrame(abl)[['config', 'acc_catboost', 'f1_catboost', 'acc_pgs', 'f1_pgs']]
abl_df.to_csv(MODELDIR / 'modality_ablation.csv', index=False)
print('\n=== Modality Ablation (Tabel 7 paper) ===')
print(abl_df.to_string(index=False))
abl_df
