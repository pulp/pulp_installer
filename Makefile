help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help               to show this message"
	@echo "  lint               to run all linters"
	@echo "  lint-ansible-lint  to run ansible-lint"
	@echo "  lint-syntax-check  to run ansible-playbook --syntax-check"

lint: lint-syntax-check lint-ansible-lint

lint-syntax-check:
	ansible-playbook deploy-pulp3.yml --syntax-check

lint-ansible-lint:
	ansible-lint deploy-pulp3.yml

.PHONY: help lint
