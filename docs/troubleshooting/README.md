# Troubleshooting

Record setup and environment failures here without revealing mission answers.

Initial categories:

- Python/package installation
- Azure CLI authentication
- Foundry project endpoint/model configuration
- authorization/access failures
- runtime/package-version mismatches


## Mission 03 session-isolation boundary

Separate these concepts when diagnosing multi-turn behavior:

1. Agent instance;
2. application user identity;
3. session creation;
4. application routing of user to session;
5. same-session conversational continuity;
6. model response wording;
7. durable persistence, which this pilot does not test.

If a fictional second user receives first-user context, inspect session routing before blaming the model. Use only synthetic identities/details when reproducing isolation defects.
