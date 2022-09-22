{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  packages = [
    (pkgs.python39.withPackages (ps: [
      ps.libgpiod
    ]))
    pkgs.mypy
    pkgs.black
    pkgs.libgpiod
    pkgs.lm_sensors
    pkgs.git
  ];
}
