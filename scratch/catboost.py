def build_features(img_name: str | None, txt_name: str | None, split: pd.DataFrame) -> np.ndarray:
    idx = split['row_id'].values
    parts = []
    if img_name is not None:
        parts.append(img_embs[img_name][idx])
    if txt_name is not None:
        parts.append(txt_embs[txt_name][idx])
    if len(parts) == 2:
        return early_fusion(parts[0], parts[1], l2_per_modality=True)
    return parts[0].astype(np.float32)


def pgs_predict_proba(model, X_test, n_virtual_ensembles: int = 30):
    """Virtual ensembles prediction untuk SGLB — return (probs, uncertainty).

    Pakai `VirtEnsembles` — return raw predictions per ensemble untuk multi-class:
    shape (n_samples, n_ensembles, n_classes). Kita average + ambil std sebagai uncertainty.

    Reference: Malinin et al. 2020 "Uncertainty in Gradient Boosting via Ensembles".
    """
    preds = model.virtual_ensembles_predict(
        X_test,
        prediction_type='VirtEnsembles',
        virtual_ensembles_count=n_virtual_ensembles,
    )
    preds = np.asarray(preds)  # (n_samples, n_ensembles, n_classes) logits

    # Softmax per ensemble
    preds_exp = np.exp(preds - preds.max(axis=-1, keepdims=True))
    probs_per_ens = preds_exp / preds_exp.sum(axis=-1, keepdims=True)

    probs = probs_per_ens.mean(axis=1)                     # (n_samples, n_classes)
    uncertainty = probs_per_ens.std(axis=1).mean(axis=1)   # scalar per sample
    return probs, uncertainty


def _fit_catboost(X_tr, y_tr, X_va, y_va, w_list,
                  iterations: int, depth: int, posterior_sampling: bool):
    """SGLB-aware fit: PGS pakai iterations 2x lebih banyak, diffusion_temperature
    lebih kecil dari default 10000, dan early_stopping diperpanjang."""
    params = dict(
        depth=depth,
        learning_rate=0.05,
        task_type='CPU',
        thread_count=-1,
        class_weights=w_list,
        loss_function='MultiClass',
        verbose=False,
        random_seed=42,
        posterior_sampling=posterior_sampling,
    )
    if posterior_sampling:
        # SGLB butuh 1.5-2x iterations (paper Ustimenko & Prokhorenkova 2020).
        # diffusion_temperature & model_shrink_rate di-auto-set oleh posterior_sampling=True,
        # jadi tidak bisa di-override manual.
        params['iterations'] = iterations * 2
    else:
        params['iterations'] = iterations

    model = CatBoostClassifier(**params)

    t0 = time()
    # SGLB: early stopping longgar agar ensemble cukup beragam
    es_rounds = 200 if posterior_sampling else 50
    model.fit(X_tr, y_tr, eval_set=(X_va, y_va), early_stopping_rounds=es_rounds)
    return model, time() - t0


def train_and_eval(img_name, txt_name, iterations: int = 1500, depth: int = 6,
                   n_virtual_ensembles: int = 30, save_dir=None):
    """Train 2 models: baseline CatBoost + SGLB (PGS). Before/after comparison."""
    X_tr, y_tr = build_features(img_name, txt_name, train), train['label_id'].values
    X_va, y_va = build_features(img_name, txt_name, val),   val['label_id'].values
    X_te, y_te = build_features(img_name, txt_name, test),  test['label_id'].values

    weights = class_weights(y_tr, num_classes=len(TARGET_CLASSES))
    w_list = [weights[i] for i in range(len(TARGET_CLASSES))]
    tag = f'{img_name}__{txt_name}'

    # --- Baseline CatBoost (no PGS) ---
    model_cb, t_cb = _fit_catboost(X_tr, y_tr, X_va, y_va, w_list,
                                    iterations, depth, posterior_sampling=False)
    y_pred_cb = model_cb.predict(X_te).flatten().astype(int)
    acc_cb = accuracy_score(y_te, y_pred_cb)
    f1_cb  = f1_score(y_te, y_pred_cb, average='macro')

    # --- CatBoost + SGLB (PGS) ---
    model_pgs, t_pgs = _fit_catboost(X_tr, y_tr, X_va, y_va, w_list,
                                      iterations, depth, posterior_sampling=True)
    probs_pgs, uncertainty = pgs_predict_proba(model_pgs, X_te, n_virtual_ensembles)
    y_pred_pgs = probs_pgs.argmax(axis=1)
    acc_pgs = accuracy_score(y_te, y_pred_pgs)
    f1_pgs  = f1_score(y_te, y_pred_pgs, average='macro')

    if save_dir is not None:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        model_cb.save_model(save_dir / f'{tag}__cb.cbm')
        model_pgs.save_model(save_dir / f'{tag}__pgs.cbm')

    del model_cb, model_pgs

    return {
        'image': img_name, 'text': txt_name,
        'acc_catboost': acc_cb, 'f1_catboost': f1_cb,
        'acc_pgs':      acc_pgs, 'f1_pgs':     f1_pgs,
        'delta_acc':    acc_pgs - acc_cb,
        'delta_f1':     f1_pgs - f1_cb,
        'mean_uncertainty': float(np.mean(uncertainty)),
        'train_sec_cb':  t_cb,
        'train_sec_pgs': t_pgs,
    }
