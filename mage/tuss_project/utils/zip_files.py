import zipfile
import requests
import os


class ZipFiles():
    def __ini__(self):
        pass
    
    def download_file(
            self,
            url: str
    ) -> str:
        '''
        Download a file passing the URL

        Args:
            url:
                string with the URL to download the file

        Returns:
            path of the downloaded file
        '''
        
        local_filename = url.split('/')[-1]

        with requests.get(url, stream=True) as r:
            if r.status_code == 200:
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            else:
                return 'It was no possible to download the file'

        return os.path.abspath(f'{local_filename}')
    
    def unpack_zip_file(
            self,
            file_to_unpack: str,
            folder: str,
            one_level: bool=False,
            unpack_nested: bool = True,
            filter: str = '.*'
    ) -> None:
        """
        Unpack a zip file

        Args:
            file_to_unpack:
                name of the zip file as string
            folder:
                destination directory of the files from inside the zip file
            one_level:
                set True to extract all files to the same folder level. 
                Default ``False``
            unpack_nested:
                set to True to unpack even the nested zip files. 
                Default ``False``
            filter: 
                name of file extension to ignore on unpacking. 
                Default ``*``

        Returns:
            None
        """
        self.__unpack(file=file_to_unpack, folder=folder, filter=filter)

        if unpack_nested is True and one_level is False:
            unpacked_folder = f"{folder}/{file_to_unpack.split('.')[0].split('/')[-1]}"
            files = self.__list_files_in_folder(unpacked_folder)

            for i in files:
                if i.name.endswith('zip'):
                    self.__unpack(
                        file=i.path,
                        folder=unpacked_folder,
                        filter=filter
                    )
        
        elif unpack_nested is False and one_level is True:
            pass

        elif unpack_nested is True and one_level is True:
            unpacked_folder = f"{folder}/{file_to_unpack.split('.')[0].split('/')[-1]}"
            files = self.__list_files_in_folder(unpacked_folder)

            for i in files:
                if i.name.endswith('zip'):
                    self.__unpack(
                        file=i.path,
                        folder=unpacked_folder,
                        filter=filter
                    )
            
            folders = self.__separate_files_folders(unpacked_folder)[1]

            self.move_files(folders=folders)

        return None
    
    def __unpack(
            self, 
            file: str,
            folder: str,
            filter: str
    ) -> None:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            for obj in zip_ref.filelist:
                if not obj.filename.endswith(filter):
                    try:
                        zip_ref.extract(obj, path=folder)
                    except zipfile.zlib.error:
                        print(f'Error trying to extract {obj.filename}')
        
        os.remove(file)

    def __list_files_in_folder(
            self, 
            folder: str
    ) -> list[os.DirEntry]:
        '''
        It makes a list of files base on a folder

        Args:
            folder: folder to scan

        Returns:
            A list with the path of zip files
        '''
        files, folders = self.__separate_files_folders(folder=folder)

        while len(folders) > 0:
            f1, f2 = self.__separate_files_folders(folders[0])

            files.extend(f1)

            folders = f2
        
        return files
    
    def __separate_files_folders(
            self,
            folder: str
    ) -> [list[str], list[str]]:
        files, folders = [], []

        for file in os.scandir(folder):
            if os.path.isfile(file):
                files.append(file)
            else:
                folders.append(file)
        
        return files, folders

    def move_files(
            self, 
            folders: str
    ) -> str:
        '''
        Move all files one level up at untill it gets the folder passed in the function parameter
        '''
        
        for folder in folders:
            for file in os.scandir(folder):
                # move all files
                os.rename(
                    file.path,

                    # move the file one level up
                    f'{os.path.dirname(os.path.dirname(file.path))}/{file.name}'
                )
                
            # delete folder
            try:
                os.rmdir(folder)
            except os.OSError:
                print('Non-empty folder')

            # go one level up
        return str(os.path.dirname(folder))
