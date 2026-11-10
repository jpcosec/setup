# Build context: source-only pi-mono checkout, locally built wheels/, and uv.
# The base is the existing Scion image, retained at its original version.
ARG BASE_IMAGE=scion-pi:latest
FROM ${BASE_IMAGE}
USER root
ARG PI_COMMIT=e9ba9e2ebce1b49dca85ab20007038c06e486ea5
LABEL io.setup.pi.source="https://github.com/jpcosec/pi-mono" \
      io.setup.pi.revision="${PI_COMMIT}" \
      io.setup.pi.version="0.67.3"

# All Pi packages resolve to the fork's locked local workspaces.
RUN npm uninstall -g @mariozechner/pi-coding-agent
COPY pi-mono/ /opt/pi-mono/
WORKDIR /opt/pi-mono
RUN npm ci --no-audit --no-fund \
 && ./node_modules/.bin/tsgo -p packages/tui/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/ai/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/agent/tsconfig.build.json \
 && ./node_modules/.bin/tsgo -p packages/coding-agent/tsconfig.build.json \
 && npm run copy-assets --workspace @mariozechner/pi-coding-agent \
 && chmod +x packages/coding-agent/dist/cli.js \
 && ln -s /opt/pi-mono/packages/coding-agent/dist/cli.js /usr/local/bin/pi \
 && test "$(pi --version 2>&1)" = 0.67.3

# DeskOps requires Python 3.12; the existing image's system Python is 3.11.
# Wheels come from source-only snapshots of the local SLDB and DeskOps checkouts.
COPY uv /usr/local/bin/uv
COPY wheels/ /opt/setup-wheels/
ENV UV_PYTHON_INSTALL_DIR=/opt/python
RUN uv venv --python 3.12 /opt/deskops-tools \
 && uv pip install --python /opt/deskops-tools/bin/python /opt/setup-wheels/*.whl \
 && chmod -R a+rX /opt/python /opt/deskops-tools
ENV PATH="/opt/deskops-tools/bin:${PATH}"
COPY launch.py /usr/local/lib/scion-pi/launch.py
RUN deskops --help >/dev/null && sldb --help >/dev/null
WORKDIR /workspace
CMD ["pi"]
