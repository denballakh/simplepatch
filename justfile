# https://just.systems/man/en/
set fallback

J := just_executable() + ' --justfile ' + justfile()

# use it like this:
# {{enter_env}} CMD -- ARGS...
enter_env := 'devenv --quiet shell'

# called by default when no recipe is specified
[default]
@_default:
  {{J}} --list --unsorted --color always

[positional-arguments]
@test-pytest *args:
    {{enter_env}} python -- -m pytest --tb=short "$@"

@test-typecheck:
    {{enter_env}} ty -- check

@test-fmt:
    {{enter_env}} ruff -- format --check . || echo "NOTE: `just fmt` might fix that"

@update-snapshots *args:
    find tests -type d -name ".snapshots" -prune -exec rm -rf {} \;
    UPDATE_SNAPSHOTS=1 {{enter_env}} python -- -m pytest "$@"

# run all tests
test: test-pytest test-typecheck test-fmt

# format all files
@fmt:
    {{enter_env}} ruff -- format .

# run the simplepatch cli
[no-exit-message]
[positional-arguments]
@cli *args:
    {{enter_env}} python -- -m simplepatch "$@"

# run python with all dependencies installed
[no-exit-message]
[positional-arguments]
@py *args:
    {{enter_env}} python -- "$@"

debug:
    #!/usr/bin/env bash
    shopt -s globstar nullglob

    SEARCH_DIR=~/YaSONiC/patches

    for file in "$SEARCH_DIR"/**/*.patch; do
        echo -n "$file... "
        
        # Get output filename by replacing extension
        outfile="${file%.patch}.patch"
        
        # Capture stdout, let stderr go to /dev/null
        if output=$(python -m simplepatch convert --from git "$file" 2>/dev/null); then
            echo "$output" > "$outfile"
            echo -e "\033[32mOK\033[0m"
        else
            echo -e "\033[31mERR\033[0m"
        fi
    done
