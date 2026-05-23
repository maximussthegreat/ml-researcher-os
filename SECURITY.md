# Security Policy

`ml-researcher-os` may eventually interact with model APIs, local files, datasets, credentials, and remote services. Treat all agent workflows as potentially sensitive.

## Report a vulnerability

Open a private security advisory if available, or contact the maintainer through GitHub.

Please include:

- affected version or commit
- reproduction steps
- expected impact
- whether credentials, private data, or remote execution are involved

## Security principles

- Never ask users to paste secrets into prompts.
- Prefer local config files with ignored secret paths.
- Make tool permissions explicit.
- Keep generated scripts inspectable.
- Default to dry-run behavior for destructive actions.

