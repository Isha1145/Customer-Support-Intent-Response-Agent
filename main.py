# (=== Intent classification ===
#                      precision    recall  f1-score   support
#
#      account_access       0.70      0.41      0.52        17
#     billing_dispute       0.74      0.67      0.70        21
#           bug_crash       0.90      0.33      0.48        80
# complaint_sentiment       0.00      0.00      0.00        17
#     feedback_praise       0.05      0.33      0.08         6
#              how_to       0.00      0.00      0.00         0
#       product_usage       0.00      0.00      0.00        35
#    resolved_closing       0.00      0.00      0.00        19
#   security_incident       0.00      0.00      0.00         0
#    spam_irrelevant       0.00      0.00      0.00         4
#   subscription_mgmt       0.00      0.00      0.00         0
#
#            accuracy                           0.25       199
#           macro avg       0.22      0.16      0.16       199
#        weighted avg       0.50      0.25      0.31       199
#
# === Escalation decision ===
# Precision: 0.296  Recall: 0.170  F1: 0.216
# (Recall matters most here: a missed escalation is worse than an unnecessary one.)
#
# === Reminder: report these alongside a trivial and a simple baseline ===
# - Trivial: majority-class intent, always-auto-handle
# - Simple: keyword-based intent classifier)
