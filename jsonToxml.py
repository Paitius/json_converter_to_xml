import json
import os
import sys
import datetime
import shutil 
from json.decoder import JSONDecodeError
from pathlib import Path

def files(path_files: Path):
    """
    Function check and list the files in specified path then return this list
    if the path does not exist rise error
    """
    try:
        if os.path.isdir(path_files):
            files = []
            for file in list(os.listdir(path_files)):
                if file.endswith(".json"):
                    files.append(file)
            return files
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        return True


def write_log_to_file(log_path : Path,log_to_save : str):
    """
    Function that saves logs
    """
    log_file = open(f'{log_path}/log_file.txt', 'a')
    log_file.write(f'{log_to_save}\n')
    log_file.close()



class Converter:
    """
    Converter encapsulates a file:list , source_path:Path and destination path:Path
    """
    def __init__(self, file:list, source_path:Path, destination_path:Path):
        """
        Construct a new 'Converter' object

        :param file: File to converted
        :parm source_path:  path to the folder
        :parm estination_path: file path to moved and saved after conversion
        :parm xml_text: empty string for conversion result
        :parm path: path to file to be converted
        :parm f: Steam of file in mode 'r'
        """
        self.file = file
        self.destination_path = destination_path
        self.xml_text = str("")
        self.path = str(f'{source_path}/{self.file}')
        self.f = open(self.path,encoding = 'UTF-8')
        self.date_file = json.load(self.f)

    def get_path(self):
        """
        Getter for path
        :return: path 
        """
        return self.path

    def get_data_file(self):
        """
        Getter data file
        :return: file content
        """
        return self.date_file

    def get_xml_text(self):
        """
        Getter xml text
        :return: xml text as string
        """
        return self.xml_text
    
    def convert_json_to_xml(self):
        """
        Convert json file to xml
        converted json from 
        :parm date_file:
        save as string to
        :parm xml_text:
        finnaly close file
        """
        result = [f'<?xml version="1.0" encoding="UTF-8"?> \n']
        result.append(f'<FLIGHT>\n')
        for k, v in self.date_file['FLIGHT'].items():
            result.append(f'  <{k}>{v}</{k}>\n')
    
        result.append(f'</FLIGHT>\n')
        self.xml_text = "".join(line for line in result)
        self.f.close()
        

    def override_move_file(self):
        """
        Overwrites json data as converted xml 
        :parm f: Steam of file in mode 'w'
        ready file moves to :parm destination_path:
        :return True: status to check later if  the file has moved
        """
        self.f = open(self.path,"w", encoding = 'UTF-8')
        self.f.write(self.xml_text)
        new_file_name = os.path.join(self.destination_path,self.file[0:-4] + "xml")
        self.f.close()
        shutil.move(self.path, new_file_name)
        return True



if __name__ == "__main__":

    input_data_path = Path(sys.argv[1])
    output_data_path = Path(sys.argv[2])
    """
    :parm log_path: path to save status of converted files
    """
    log_path = Path('./')
    write_log_to_file(log_path,f'script started working at: {datetime.datetime.now(datetime.UTC)}')
    try:
        while True:
            files_list_to_convert = []
            if files(input_data_path) == True:
                print(f'Path do not exist, script stopped working at: ', datetime.datetime.now(datetime.UTC))
                break
            else:
                files_list_to_convert = files(input_data_path)
                

            print(files_list_to_convert)
            for (file_to_converted) in files_list_to_convert:
                try:
                    converter = Converter(file_to_converted,input_data_path, output_data_path)
                    converter.convert_json_to_xml()
                    if converter.override_move_file():
                         write_log_to_file(log_path,f'{file_to_converted},converted, correctly, {datetime.datetime.now(datetime.UTC)}')
                except IOError as err:
                    write_log_to_file(log_path, f'{file_to_converted},IOError, Cannot open file. Please check the file exists and is closed,{datetime.datetime.now(datetime.UTC)}')
                except JSONDecodeError:
                    write_log_to_file(log_path, f'{file_to_converted},JSONDecodeError, data deserialization,{datetime.datetime.now(datetime.UTC)} ')             
                finally:
                    continue
                    
  
    finally:
        write_log_to_file(log_path,f'script stopped working at: {datetime.datetime.now(datetime.UTC)}')
    