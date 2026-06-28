---
title: Explainable Ensemble Learning for Cardiovascular Risk Stratification
authors: Pranshu Kumar
venue: International Conference on Applied Machine Learning in Healthcare (AMLH)
year: 2024
doi: placeholder
status: published
keywords: [Cardiovascular prediction, Ensemble learning, Explainable AI, SHAP, Clinical decision support]
related_project: cardiorisk
pdf: null
---

## Abstract

Proposes a two-model ensemble combining XGBoost and Logistic Regression on the 920-patient UCI Heart Disease dataset achieving AUC-ROC 0.905 with 5-fold cross-validation. SHAP values expose dominant clinical risk features enabling physician-interpretable risk stratification. Results demonstrate that ensemble calibration is as critical as raw accuracy in clinical deployment contexts.

## Motivation

Cardiovascular disease diagnosis depends on clinical intuition applied to multi-dimensional patient data. ML models can systematise this process — but only if clinicians can understand and trust the output. This work addresses the interpretability gap in clinical ML deployment.

## Key Findings

- XGBoost + LR ensemble outperforms either model alone (AUC 0.905 vs 0.871 solo)
- SHAP analysis identifies chest pain type and maximum heart rate as dominant predictors
- Calibration curve analysis shows model is reliable at all risk thresholds

## Future Work

Extend to multi-disease risk prediction. Add longitudinal tracking for repeated assessments over time.
