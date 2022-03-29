
.ONESHELL:

SHELL=/bin/bash

CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

.PHONY: check_conda_installed check_environment_created

run: setup
	$(CONDA_ACTIVATE) ProSolAdv
	python app.py

setup: check_conda_installed check_environment_created

check_environment_created: check_conda_installed environment.yml
	[ `conda env list | grep "^ProSolAdv\s" | wc -l` == 1 ] || conda env create -n ProSolAdv -f environment.yml

check_conda_installed:
	@which conda 2>&1 || (echo "conda is not reachable. Please install it."; exit 1)

clean:
	conda remove -n ProSolAdv --all
