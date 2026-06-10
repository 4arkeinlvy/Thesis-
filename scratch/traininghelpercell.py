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


def _fit_catboost(X_tr, y_tr, X_va, y_va, w_list,
                  iterations, depth, posterior_sampling: bool):
    model = CatBoostClassifier(
        iterations=iterations,
        depth=depth,
        learning_rate=0.05,
        task_type='CPU',               # PGS hanya support CPU
        thread_count=-1,
        class_weights=w_list,
        posterior_sampling=posterior_sampling,
        loss_function='MultiClass',
        verbose=False,
    )
    t0 = time()
    model.fit(X_tr, y_tr, eval_set=(X_va, y_va), early_stopping_rounds=50)
    return model, time() - t0


def train_and_eval(img_name, txt_name, iterations=1000, depth=6, save_dir=None):
    """Train 2 models (baseline + PGS). If save_dir, simpan .cbm per combo dan
    JANGAN return model objek → hemat RAM untuk loop panjang."""
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

    # --- CatBoost + PGS ---
    model_pgs, t_pgs = _fit_catboost(X_tr, y_tr, X_va, y_va, w_list,
                                      iterations, depth, posterior_sampling=True)
    probs_pgs, _ = pgs_predict_proba(model_pgs, X_te, n_virtual_ensembles=10)
    y_pred_pgs = probs_pgs.argmax(axis=1)
    acc_pgs = accuracy_score(y_te, y_pred_pgs)
    f1_pgs  = f1_score(y_te, y_pred_pgs, average='macro')

    # Persist to disk so bisa di-load lagi nanti (opsional)
    if save_dir is not None:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        model_cb.save_model(save_dir / f'{tag}__cb.cbm')
        model_pgs.save_model(save_dir / f'{tag}__pgs.cbm')

    # Free memory — models sudah di disk kalau save_dir di-set
    del model_cb, model_pgs

    return {
        'image': img_name, 'text': txt_name,
        'acc_catboost': acc_cb, 'f1_catboost': f1_cb,
        'acc_pgs':      acc_pgs, 'f1_pgs':     f1_pgs,
        'delta_acc':    acc_pgs - acc_cb,
        'delta_f1':     f1_pgs - f1_cb,
        'train_sec_cb':  t_cb,
        'train_sec_pgs': t_pgs,
    }
