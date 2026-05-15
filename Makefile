.PHONY: transform web-install dev build clean clean-web help

help:
	@echo "Targets:"
	@echo "  transform    Regenerate web/public/problems.json + web_harness.py + utils.py"
	@echo "  web-install  Install web/ npm dependencies (npm ci)"
	@echo "  dev          Run transform then start Astro dev server"
	@echo "  build        Run transform then build static site to web/dist/"
	@echo "  clean        Remove generated web assets (problems.json, copied py files)"
	@echo "  clean-web    Remove web/node_modules, web/dist, web/.astro"

transform:
	python build/transform.py

web-install:
	cd web && npm ci

dev: transform
	cd web && npm run dev

build: transform
	cd web && npm run build

clean:
	rm -f web/public/problems.json web/public/web_harness.py web/public/utils.py

clean-web:
	rm -rf web/node_modules web/dist web/.astro
