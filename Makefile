all:
	@echo "Please run make vars_files and provide the Version and Patch level"

vars_files:
	@python3 -m venv .varsenv
	@pip3 install -r scripts/requirements.txt
	@python3 scripts/generate.py $(filter-out $@,$(MAKECMDGOALS))
	@rm -rf vars/*.yml
	@mv scripts/vars/*.yml vars/
	@git add vars/*.yml

%:
	@: