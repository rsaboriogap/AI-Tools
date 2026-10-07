SHELL := /bin/bash
ROOT  := claude-skills
DIST  := dist
INSTALL_DIR ?= $(HOME)/.claude/skills

.PHONY: help install test lint package clean

help:
	@echo "Targets: install | test | lint | package | clean"

install:
	@mkdir -p "$(INSTALL_DIR)"
	@cp -R $(ROOT)/* "$(INSTALL_DIR)/"
	@echo "Installed to $(INSTALL_DIR)"

test:
	@python -m pytest tests/python -v

lint:
	@if command -v ruff >/dev/null 2>&1; then ruff check $(ROOT); else echo "ruff missing"; fi

package:
	@mkdir -p $(DIST)
	@zip -qr $(DIST)/claude-skills.zip $(ROOT)

clean:
	@rm -rf $(DIST) build __pycache__ .pytest_cache
