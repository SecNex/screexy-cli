# EdgeSight CLI

This is a simple CLI for EdgeSight. It is written in Python and makes the usage of EdgeSight Configuration easier.

## Installation

To install the CLI, you need to clone the repository and install the requirements.

```bash
git clone https://github.com/SecNex/edgesight-cli.git
cd edgesight-cli
pip install -r requirements.txt
chmod +x edgesight
```

**Note:** You need to have Python3 installed on your system.

```bash
python3 --version
```

## Usage

To use the CLI, you need to run the `edgesight-cli.py` script.

```bash
./edgesight --help
```

### Examples

**List all tiles**

```bash
./edgesight kiosk list
```