import subprocess
import sys
import os
import warnings


warnings.simplefilter(action='ignore', category=FutureWarning)


class Setup():
    def __init__(
            self,
            packages: list[str]
    ) -> None:
        self.packages = [package.lower() for package in packages]
        self.__upgrade_pip()

    def __upgrade_pip(self):
        print('-> Atualizando o pip (gerenciador de pacotes do python)')
        subprocess.check_call(
            [
                sys.executable, '-m',
                'pip', 'install',
                '--upgrade', 'pip', '-q',
                '--root-user-action=ignore'
            ]
        )

    def install_packages(
            self,
            check_package: bool = False
    ) -> None:
        print('-> Instalando pacotes')

        for package in self.packages:
            print(f'\tInstalando {package}')
            subprocess.check_call(
                [
                    sys.executable, "-m", #python3 -m
                    'pip', "install", package, #pip install <package>
                    '-q', '--root-user-action=ignore' #options
                ]
            )
    
    def uninstall_packages(self):
        print('-> Desinstalando pacotes')

        for package in self.packages:
            package_name = package.split('==')[0] if '==' in package else package
            package_name = package_name.lower().replace('-', '_')

            print(f'\tDesinstalando {package_name}')
            subprocess.check_call(
                [sys.executable, "-m", 'pip', "uninstall", package, '-q', '-y']
            )
