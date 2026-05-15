# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Makefile                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/12 16:27:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 09:33:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

# ===================
# =		VARIABLES	=
# ===================
PYTHON			=	python3
PDB 			=	python3 -m pdb
FLAKE8			=	uv run flake8
MYPY 			=	uv run mypy
MYPY_FLAGS		=	--warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
INSTALL_UV		=	curl -LsSf https://astral.sh/uv/install.sh | sh
CHECK_UV		=	command -v uv
UV_WARN			=	--link-mode copy
UV_SKIP_WHEEL	=	UV_SKIP_WHEEL_FILENAME_CHECK=1

# ===================
# =		RULES		=
# ===================

.PHONY:		all install run debug clean lint lint-strict delete-uv
.SILENT:

all:		install run

install:
			@if	! $(CHECK_UV) > /dev/null 2>&1; then \
					echo "$(BRED)UV not installed. Installing...$(RESET)"; \
					$(INSTALL_UV); \
			fi
			@echo "$(BGREEN)Installing project dependencies using uv...$(RESET)"
			$(UV_SKIP_WHEEL) uv sync $(UV_WARN)

run:		install
			$(PYTHON) pac-man.py

debug:		install
			@echo "$(BGREEN)Running the main script in debug mode...$(RESET)"
			$(PDB) pac-man.py

clean:
			@echo "$(YELLOW)Cleaning temporary files and caches... 🗑️$(RESET)"
			find . -type d -name "__pycache__" -exec rm -rf {} +
			find . -type f -name "*.pyc" -delete
			find . -type f -name "*.pyo" -delete
			rm -rf .mypy_cache
			rm -rf .pytest_cache

lint:
			@clear
			@echo "$(BMAGENTA)Running standard linting...$(RESET)"
			@status=0; \
			$(FLAKE8) $(LINT_TESTER) || status=$$?; \
			$(MYPY) $(LINT_TESTER) $(MYPY_FLAGS) || status=$$?; \
			exit $$status

lint-strict:
			@clear
			@echo "$(BMAGENTA)Running strict linting...$(RESET)"
			@status=0; \
			$(FLAKE8) $(LINT_TESTER) || status=$$?; \
			$(MYPY) $(LINT_TESTER) $(MYPY_FLAGS) --strict || status=$$?; \
			exit $$status

delete-uv:
			@if $(CHECK_UV) > /dev/null 2>&1; then \
					echo "$(BRED)Deleting uv...$(RESET)"; \
					rm -f $$(which uv); \
			else \
					echo "$(BRED)UV not installed. Cannot delete. Abording.$(RESET)"; \
			fi


# ===================
# =		COLORS		=
# ===================

RESET		=	\033[0m
BGREEN		=	\033[92m
BMAGENTA	=	\033[95m
YELLOW		=	\033[93m
BRED		=	\033[91m
