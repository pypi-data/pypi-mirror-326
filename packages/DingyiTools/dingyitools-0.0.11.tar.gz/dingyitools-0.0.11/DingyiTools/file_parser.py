from __future__ import annotations
from typing import Iterator
import glob
import pandas as pd


class FileParser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
    
    @property
    def paths_iterator(self) -> Iterator[str]:
        """
        该方法用于生成一个迭代器，迭代器中的元素为与 self.file_path 匹配的文件路径。

        Returns:
            Iterator[str]: 一个字符串迭代器，每个字符串代表一个匹配的文件路径。
        """
        # 使用 glob.iglob 函数生成一个迭代器，该迭代器会逐个返回与 self.file_path 匹配的文件路径
        return glob.iglob(self.file_path)
    
    @property
    def paths_list(self) -> list[str]:
        """
        该方法用于生成一个列表，列表中的元素为与 self.file_path 匹配的文件路径。

        Returns:
            list[str]: 一个字符串列表，每个字符串代表一个匹配的文件路径。
        """
        return glob.glob(self.file_path)
    
    def merge_df(self, df_iterator: Iterator[pd.DataFrame]=None) -> pd.DataFrame:
        df_ls = []
        for df in df_iterator:
            df_ls.append(df)
        return pd.concat(df_ls, ignore_index=True)

class CsvParser(FileParser):
    def read_file(self, path:str=None, **kwargs) -> pd.DataFrame:
        return pd.read_csv(path, **kwargs)
    
    def batch_read_file(self, paths_iterator: Iterator[str]=iter([]), info=False, **kwargs) -> Iterator[pd.DataFrame]:
        """
        读取指定路径的 CSV 文件，并以生成器的形式逐个返回 pandas.DataFrame 对象。

        Args:
            path (str): 要读取的 CSV 文件的路径。
            **kwargs: 传递给 pandas.read_csv 函数的可选关键字参数，
                      用于自定义 CSV 文件的读取方式，例如指定分隔符、表头、缺失值等。

        Returns:
            Iterator[pd.DataFrame]: 一个迭代器，每次迭代返回一个 pandas.DataFrame 对象，
                                    该对象包含了 CSV 文件的内容。
        """
        # 使用 pandas 的 read_csv 函数读取指定路径的 CSV 文件，
        # 并将 kwargs 中的关键字参数传递给 read_csv 函数，
        # 最后通过生成器逐个返回读取到的数据框
        for path in paths_iterator:
            if info:
                print(f"reading {path}")
            yield self.read_file(path, **kwargs)
    
    
    def merge_file(self, paths_iterator: Iterator[str]=None, info=False, **kwargs) -> pd.DataFrame:
        """
        合并多个 CSV 文件的数据到一个 DataFrame 中。

        Args:
            paths_iterator (Iterator[str], optional): 一个包含 CSV 文件路径的迭代器，默认为 None。
                                                     如果为 None，则使用 self.paths_iterator 生成的迭代器。
            info (bool, optional): 是否打印读取文件的信息，默认为 False。
            **kwargs: 传递给 pandas.read_csv 函数的可选关键字参数，
                      用于自定义 CSV 文件的读取方式，例如指定分隔符、表头、缺失值等。

        Returns:
            pd.DataFrame: 合并后的 pandas.DataFrame 对象。
        """
        # 检查 paths_iterator 是否为 None，如果是则使用 self.paths_iterator 生成的迭代器
        if not paths_iterator:
            paths_iterator = self.paths_iterator
        # 调用 self.read_csv 方法，传入 info 和 kwargs，获取一个包含多个 pandas.DataFrame 对象的迭代器
        file_iterator = self.batch_read_file(paths_iterator=paths_iterator, info=info, **kwargs)
        # 调用 self.merge_df 方法，传入 file_iterator，将多个 DataFrame 合并成一个大的 DataFrame 并返回
        return self.merge_df(file_iterator)
    
        
class ExcelParser(CsvParser):
    def read_file(self, path:str=None, **kwargs) -> pd.DataFrame:
        return pd.read_excel(path, **kwargs)