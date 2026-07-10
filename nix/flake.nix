{
  description = "Python dev environment flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
    nixpkgs-unstable.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs, nixpkgs-unstable }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    packageOverrides = pkgs.callPackage ./python-packages.nix {};
    pkgs-unstable = nixpkgs-unstable.legacyPackages.${system};

    python = pkgs.python313.override { inherit packageOverrides; };

    pythonEnv = python.withPackages (p: with p; [
      # Here goes all the libraries that can't be managed by uv because of dynamic linking issues
      # or that you just want to be managed by nix for one reason or another
      tkinter
      pyqt5
      pyserial
      pystructurizr
    ]);
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        pythonEnv
        uv
        ruff
        ty

        libsForQt5.qt5.qtwayland
      ] ++ [
        pkgs-unstable.act
      ];

      shellHook = ''
        export UV_PYTHON_PREFERENCE="only-system";
        export UV_PYTHON=${python}
      '';

      env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib
        pkgs.libz
        pkgs.xorg.libX11
        pkgs.libGL
      ];
    };
  };
}
