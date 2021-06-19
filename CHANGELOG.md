# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2021-06-19 :droplet:
- Restores support for enums on examples `@dataclasses`, after the fix
  implemented in `0.1.3`
- Adds support for built-in `UUID`, `time`, `date`, `datetime`, `bytes`,
  handling in examples for `YAML` format
- Adds `partial-time` ValueFormat for `time` (see
  https://xml2rfc.tools.ietf.org/public/rfc/html/rfc3339.html#anchor14)

## [0.1.3] - 2021-06-17 :droplet:

- Corrects a bug forcing `camelCase` on examples objects handled as dataclasses
- Adds base64 ValueFormat to the v3 enum
## [0.1.2] - 2021-05-03 :notes:

- Adds a changelog
- Adds a code of conduct
- Updates `PyYAML` dependency to version `5.4.1`
