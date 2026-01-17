# PyCV

A Python tool to generate a CV as PDF from a TOML configuration file.

## Setup

Run the setup script to install dependencies and initialize your configuration file:

```bash
./setup.sh
```

This will copy `config/data.toml.example` to `config/data.toml` if it does not already exist.

## Configuration

All CV data is stored in `config/data.toml`. Edit this file to update your information.

The configuration is organized into the following sections:

- **[profile]**: Personal details, contact information, and summary.
- **[[education]]**: List of degrees and schools.
- **[skills]**: List of skills (under `list` key).
- **[[experience]]**: Work history with highlights.
