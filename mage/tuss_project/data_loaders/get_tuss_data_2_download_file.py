if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from tuss_project.utils.zip_files import ZipFiles
from datetime import date
import os
from dateutil import relativedelta


def get_previous_month(months: int) -> tuple[int]:
    previous_month = str(date.today() + relativedelta.relativedelta(months=months * -1))
    previous_month = previous_month.split('-')

    return previous_month[1], previous_month[0]


@data_loader
def load_data(*args) -> dict:
    """
    Template code for downloading data from brazilian system of health, especically the TUSS codes.

    Returns:
        The path of the downloaded file, it could be empty if the file
        was not downloaded because some error occoured
    """
    ano = os.getenv('ANO')
    mes = os.getenv('MES')

    if not ano and not mes:
        current_date = date.today()
        mes = f'{current_date.month:02d}'
        ano = str(current_date.year)

    url = f'https://www.ans.gov.br/arquivos/extras/tiss/Padrao_TISS_Representacao_de_Conceitos_em_Saude_{ano}{mes}.zip'

    file = ZipFiles()
    downloaded_file_path = file.download_file(url=url)

    counter = 1

    while downloaded_file_path == 'It was no possible to download the file':
        print(f'It was not possible to download the file for {mes}/{ano}.')
        print('Trying 1 month behind.')
        mes, ano = get_previous_month(counter)
        url = f'https://www.ans.gov.br/arquivos/extras/tiss/Padrao_TISS_Representacao_de_Conceitos_em_Saude_{ano}{mes}.zip'
        downloaded_file_path = file.download_file(url=url)
        counter += 1

    return {
        'downloaded_file_path': downloaded_file_path,
        'mes': mes,
        'ano': ano
    }


@test
def test_output(output: dict) -> None:
    """
    Template code for testing the output of the block.
    """
    ano = output.get('ano')
    mes = output.get('mes')
    file_path = output.get('downloaded_file_path')

    assert f'{ano}{mes}' in file_path, "Download failed or file couldn't be found"
