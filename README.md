# ShiftIQ CLI

This is a simple CLI for ShiftIQ. It is written in Python and makes the usage of ShiftIQ Configuration easier.

## Installation

To install the CLI, you need to clone the repository and install the requirements.

```bash
git clone https://github.com/SecNex/shifiq-cli.git
cd shifiq-cli
pip install -r requirements.txt
chmod +x shifiq
```

**Note:** You need to have Python3 installed on your system.

```bash
python3 --version
```

## Usage

To use the CLI, you need to run the `shifiq-cli.py` script.

```bash
./shifiq --help
```

### Examples

**List all tiles**

```bash
./shifiq kiosk list
```