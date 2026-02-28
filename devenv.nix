# https://devenv.sh/reference/options/
{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  # https://devenv.sh/packages/
  packages = [
    pkgs.git
    pkgs.just
    pkgs.ruff
    pkgs.ty
  ];

  languages.python = { # https://devenv.sh/reference/options/#languagespythonenable
    enable = true;
    package = pkgs.python314;

    venv.enable = true;
    venv.requirements = ./requirements.txt;

    # uv.enable = true;
  };

}
