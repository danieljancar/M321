# M321 Operations Guide

This repository contains a collection of automation scripts and mission walkthroughs
used to interact with the external "M321" simulation services (stations, cargo
management, communications relays, etc.). Most scripts are small Python utilities
that call the HTTP and XML-RPC endpoints documented in the various `*_aufgaben`
(mission) folders.

## Prerequisites

* **Python 3.10+** – the code relies on standard library modules that ship with
  recent CPython releases.
* **pip** for installing Python dependencies.
* **curl** (optional) for the missions that provide raw HTTP command sequences.

> ℹ️ The scripts talk to services that are expected to be reachable at
> `http://10.255.255.254:<port>/…`. Make sure you have network access to that
> environment before attempting to run any mission scripts.

## Initial setup

Clone the repository and install the Python dependencies into an isolated
virtual environment:

```bash
git clone <repo-url>
cd M321
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The modules expect the repository root to be on your `PYTHONPATH`. You can do
this ad-hoc when launching a script:

```bash
export PYTHONPATH="${PWD}"
```

> ✅ **Tip:** keep the `=` in the command above. Omitting it (for example,
> running `export PYTHONPATH PWD`) leaves `PYTHONPATH` unchanged and the
> imports will still fail. If you are inside the virtual environment you can
> also append to an existing value with `export PYTHONPATH="${PWD}:${PYTHONPATH}"`.

(If you prefer, add the export to the end of `.venv/bin/activate` so it is set
whenever the virtual environment is activated.)

## Running missions and scripts

Mission walkthroughs live inside the `*_aufgaben` folders. Each folder contains
Python helper scripts plus (sometimes) a `*.txt` file with the sequence of HTTP
calls required for that mission. Typical usage patterns are:

* **Execute a Python helper** – for example, to automate an iron trading loop:

  ```bash
  export PYTHONPATH="${PWD}"
  python -m leonarda_aufgaben.buy_and_sell_iron
  ```

  Most helpers run indefinitely until you interrupt them with `Ctrl+C`.

* **Follow a text walkthrough** – `matsu_toshi_aufgaben/matsu_toshi_aufgabe.txt`
  lists the exact `curl` calls and the companion scripts (for example,
  `python -m matsu_toshi_aufgaben.artemis_coms`) that must be executed at each
  step. Run each command in order from a shell where the virtual environment and
  `PYTHONPATH` are already configured.

* **Leverage shared utilities** – modules in the repository root provide
  reusable building blocks:

  | Module | Purpose |
  | --- | --- |
  | `navigation.py` | Travel between stations/coordinates and trigger trade actions. |
  | `communication.py` | Wrapper around station buy/sell/item HTTP endpoints. |
  | `cargo_hold.py` | Inspect and rearrange the cargo hold layout. |
  | `scanner.py`, `energy.py`, etc. | Direct HTTP clients for the corresponding ship systems. |

  You can import these modules in new mission scripts once `PYTHONPATH` points to
  the repository root.

## Directory overview

* `leonarda_aufgaben/` – resource farming/trading automation scripts.
* `matsu_toshi_aufgaben/` – mixed missions involving navigation and encoded
  communications; includes text walkthrough instructions.
* `major_green_aufgaben/`, `mechatrix_velox_aufgaben/`, `nuku_aufgaben/` –
  additional mission folders that follow the same pattern (scripts plus any
  mission notes).
* `setup/` – supplemental station-specific setup notes.
* `k8s/` – Kubernetes manifests and related tooling (not required for the basic
  mission scripts but useful for infrastructure deployments).

Explore each folder to find mission-specific instructions; the naming usually
matches the in-game station or NPC associated with the task.

## Troubleshooting

* **`ModuleNotFoundError` for project modules** – confirm that `PYTHONPATH` is set
  to the repository root (see above). You can verify the setting with
  `python -c "import navigation, communication"`; if it prints nothing, the
  imports succeeded.
* **`ModuleNotFoundError` for third-party libraries** – ensure you installed the
  requirements inside the active virtual environment. If you only need the HTTP
  helpers, installing `requests` is sufficient:

  ```bash
  pip install requests
  ```

  (When available, `pip install -r requirements.txt` keeps the rest of the
  optional tooling in sync.)
* **HTTP errors/timeouts** – verify connectivity to the mission environment and
  confirm that the ship is in the expected state before running a script.

With the environment prepared you can mix and match the provided helpers or
write your own automation scripts on top of the HTTP APIs exposed by the
simulation. 
