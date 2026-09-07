# Herdr runtime contract

Herdr is an external runtime dependency. Setup stores only the declarative
contract and integration defaults; it does not vendor Herdr or persist Herdr
pane, tab, process, or workspace IDs.

Opsys/DeskOps owns the semantic desk and execution plan. The adapter materializes
one Herdr workspace per desk, then creates tabs and panes before starting agents
or ordinary processes.

The adapter should capture IDs from Herdr JSON responses and persist them only as
runtime references in the corresponding execution state. A missing workspace is
reconstructible from the durable desk and execution documents.

