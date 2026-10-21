.PHONY: data metric-a clean
data:
	uv run generate.py
metric-a: data
	uv run compute.py
clean:
	rm -rf data
