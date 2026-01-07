{
  description = "led-name-badge-ls32: Nix dev shell (pyusb + pillow + HIDAPI) + optional NixOS udev module";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    # This upstream repo provides the Python module `hidapi` (NOT `pyhidapi`).
    pyhidapi-src.url = "github:awelkie/pyhidapi";
    pyhidapi-src.flake = false;
  };

  outputs = { self, nixpkgs, flake-utils, pyhidapi-src }:
    let
      lib = nixpkgs.lib;
    in
    (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        # Python version with good nixpkgs coverage
        python = pkgs.python312;
        py = python.pkgs;

        # Build awelkie/pyhidapi, which installs the importable module `hidapi`
        hidapi_python = py.buildPythonPackage {
          pname = "hidapi-python";
          version = "1.0.0";
          src = pyhidapi-src;
          format = "setuptools";
          propagatedBuildInputs = [ pkgs.hidapi ];
          doCheck = false;
        };

        # Compatibility shim so this repo can `import pyhidapi`
        # (re-exporting from `hidapi.hidapi`)
        pyhidapi_compat = py.buildPythonPackage {
          pname = "lednamebadge-pyhidapi-compat";
          version = "0.0.0";
          src = pkgs.runCommand "pyhidapi-compat-src" {} ''
            mkdir -p $out/pyhidapi
            cat > $out/pyhidapi/__init__.py <<'PY'
# Compatibility shim for led-name-badge-ls32 which does: `import pyhidapi`
from hidapi.hidapi import *  # noqa: F401,F403
PY
            cat > $out/setup.py <<'PY'
from setuptools import setup
setup(
  name="lednamebadge-pyhidapi-compat",
  version="0.0.0",
  packages=["pyhidapi"],
)
PY
          '';
          format = "setuptools";
          propagatedBuildInputs = [ hidapi_python ];
          doCheck = false;
        };

        pythonEnv = python.withPackages (ps: with ps; [
          pillow
          pyusb
          pyhidapi_compat
        ]);

        ldLibPath = pkgs.lib.makeLibraryPath [
          pkgs.hidapi
          pkgs.libusb1
          pkgs.stdenv.cc.cc.lib
        ];

        # Option B1: a single wrapper command that does sudo + LD_LIBRARY_PATH for you.
        # Usage:
        #   led-badge -M hidapi "I:HEART2:you"
        #
        # It assumes you run it from the repo directory (so $PWD/led-badge-11x44.py exists).
        ledBadge = pkgs.writeShellScriptBin "led-badge" ''
          set -euo pipefail
          exec sudo env \
            "LD_LIBRARY_PATH=${ldLibPath}" \
            "${pythonEnv}/bin/python3" \
            "$PWD/led-badge-11x44.py" \
            "$@"
        '';
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.libusb1
            pkgs.hidapi
            pkgs.udev
            ledBadge
          ];

          # Still helpful for *non-sudo* runs / debugging
          LD_LIBRARY_PATH = ldLibPath;

          shellHook = ''
            echo "LED badge dev shell ready."
            echo
            echo "Try:"
            echo "  led-badge -M hidapi \"I:HEART2:you\""
            echo
	    echo "Write to multiple Memorybanks:"
	    echo
            echo '  led-badge -s 7,4,7,6 -m 0,4,0,0 ":bicycle:" ":ball:" "Fast scrolling Text" "Other fast text" ":happy:" ":happy2:"'
	    echo
          '';
        };
      }
    ))
    //
    {
      nixosModules.default = { config, lib, ... }:
        let
          cfg = config.services.led-name-badge-ls32;
        in
        {
          options.services.led-name-badge-ls32 = {
            enable = lib.mkEnableOption "udev permissions for led-name-badge-ls32 (hidraw uaccess)";

            idVendor = lib.mkOption {
              type = lib.types.str;
              default = "0416";
              example = "0416";
              description = "USB vendor id (hex, 4 chars) for the badge.";
            };

            idProduct = lib.mkOption {
              type = lib.types.str;
              default = "5020";
              example = "5020";
              description = "USB product id (hex, 4 chars) for the badge.";
            };
          };

          config = lib.mkIf cfg.enable {
            services.udev.extraRules = ''
              # led-name-badge-ls32 (hidraw) — allow active desktop user access (no sudo)
              KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="${cfg.idVendor}", ATTRS{idProduct}=="${cfg.idProduct}", TAG+="uaccess"
            '';
          };
        };
    };
}

