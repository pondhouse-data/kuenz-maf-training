FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.12.10 /uv /uvx /usr/local/bin/
# Geerbte, hier ungenutzte Yarn-Quelle mit veraltetem Signaturschlüssel entfernen.
RUN rm -f /etc/apt/sources.list.d/yarn.list
