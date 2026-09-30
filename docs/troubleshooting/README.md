# Troubleshooting

Record setup and environment failures here without revealing mission answers.

Initial categories:

- Python/package installation
- Azure CLI authentication
- Foundry project endpoint/model configuration
- authorization/access failures
- runtime/package-version mismatches


## Mission 02 diagnostic boundary

When investigating tool behavior, separate these layers:

1. environment/authentication;
2. agent tool selection;
3. tool arguments;
4. Python tool/source execution;
5. raw tool result;
6. model interpretation/final wording.

If the environment fails before the tool runs, restore setup first. If the raw tool result is already wrong, investigate the source before changing the model or prompt. If the raw result is correct but the final answer is wrong, investigate model interpretation.
