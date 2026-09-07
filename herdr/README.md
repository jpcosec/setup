# Herdr runtime contract

Herdr is an external runtime dependency. Setup stores only the declarative
contract and integration defaults; it does not vendor Herdr or persist Herdr
pane, tab, process, or workspace IDs.

## Initialize Opsys

```bash
/home/jp/setup/install/init-herdr.sh
```

This creates one `opsys` Space using the local Opsys/DeskOps repository as its
working directory, with Neovim, Yazi, and tests. Add `--agents` to start the
executor and tester Pi agents. The printed Herdr IDs are runtime references;
do not copy them into configuration files.

Opsys/DeskOps owns the semantic desk and execution plan. The adapter materializes
one Herdr workspace per desk, then creates tabs and panes before starting agents
or ordinary processes.

The adapter should capture IDs from Herdr JSON responses and persist them only as
runtime references in the corresponding execution state. A missing workspace is
reconstructible from the durable desk and execution documents.
