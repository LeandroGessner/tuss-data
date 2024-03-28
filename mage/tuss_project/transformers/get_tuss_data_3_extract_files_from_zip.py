if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
from tuss_project.utils.zip_files import ZipFiles


@transformer
def transform(data):
    """
    This block extracts all the files from the
    zip file downloaded in the previews block.

    Args:
        data: The output from the upstream parent block

    Returns:
        Nothing
    """
    files = ZipFiles()

    file_to_unpack: str = data.get('downloaded_file_path')

    files.unpack_zip_file(
        file_to_unpack = file_to_unpack,
        folder = 'tuss_project',
        one_level = True,
        filter = '.pdf'
    )
