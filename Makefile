.PHONY: validate

validate:
	uv run pytest
	python scripts/voice_lint.py
	python scripts/spec_check.py
	python scripts/validate_pillar_schema.py

