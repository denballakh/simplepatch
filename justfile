# https://just.systems/man/en/
set fallback

J := just_executable() + ' --justfile ' + justfile()

# called by default when no recipe is specified
[default]
@_default:
  {{J}} --list --unsorted --color always

test-pytest *args:
    pytest "$@"

test-typecheck:
    ty check

test-fmt:
    ruff format --check .

test: test-pytest test-typecheck test-fmt

fmt:
    ruff format .


clean:
    git clean -fxd

cli *args:
    python -m simplepatch "$@"
