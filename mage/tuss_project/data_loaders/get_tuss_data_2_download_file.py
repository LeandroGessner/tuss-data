if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from tuss_project.utils.zip_files import ZipFiles


@data_loader
def load_data(**kwargs):
    """
    Template code for loading data from brazilian system of health.

    Returns:
        The path of the downloaded file, it could be empty if the file
        was not downloaded because some error occoured
    """
    ano = kwargs['ANO']
    mes = kwargs['MES']

    url = f'https://www.ans.gov.br/arquivos/extras/tiss/Padrao_TISS_Representacao_de_Conceitos_em_Saude_{ano}{mes}.zip'

    file = ZipFiles()
    downloaded_file_path = file.download_file(url=url)

    return downloaded_file_path


@test
def test_output(output, **kwargs) -> None:
    """
    Template code for testing the output of the block.
    """
    ano = kwargs['ANO']
    mes = kwargs['MES']

    assert f'{ano}{mes}' in output, "Download failed or file couldn't be found"