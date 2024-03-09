if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from tuss_project.custom.general_setup import Setup
import warnings


@custom
def transform_custom() -> None:
    """
    Returns:
        None
    """
    
    libs = [
        'requests', 'unidecode', 'polars'
    ]

    setup = Setup(libs)
    setup.install_packages()
