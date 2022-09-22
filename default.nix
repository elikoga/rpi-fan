{ pkgs ? import <nixpkgs> { }
, python39 ? pkgs.python39
, lm_sensors ? pkgs.lm_sensors
,
}:
let
  python = pkgs.python39.withPackages (ps: [
    ps.libgpiod
  ]);
in
pkgs.writeShellScript "fan-control" ''
  export PATH=${lm_sensors}/bin:$PATH
  ${python}/bin/python3 ${./main.py}
''
