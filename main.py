import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib


def calculate_hash(file_path: str, algorithm: str) -> str:
    if algorithm == 'SHA2-256':
        hash_obj = hashlib.sha256()
    elif algorithm == 'SHA2-512':
        hash_obj = hashlib.sha512()
    elif algorithm == 'SHA3-256':
        hash_obj = hashlib.sha3_256()
    elif algorithm == 'SHA3-512':
        hash_obj = hashlib.sha3_512()
    else:
        raise ValueError(f"不支持的哈希算法: {algorithm}")

    chunk_size = 8192
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def compare_hashes(hash1: str, hash2: str) -> bool:
    return hash1.lower() == hash2.lower()


SUPPORTED_ALGORITHMS = ['SHA2-256', 'SHA2-512', 'SHA3-256', 'SHA3-512']


class HashValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件哈希校验工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        self.file_path_1 = tk.StringVar()
        self.file_path_2 = tk.StringVar()
        self.input_hash = tk.StringVar()
        self.result_hash = tk.StringVar()
        self.algorithm = tk.StringVar(value='SHA2-256')

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_calc = ttk.Frame(notebook)
        self.tab_compare_hash = ttk.Frame(notebook)
        self.tab_compare_files = ttk.Frame(notebook)

        notebook.add(self.tab_calc, text='哈希值计算')
        notebook.add(self.tab_compare_hash, text='哈希值比对')
        notebook.add(self.tab_compare_files, text='文件检验')

        self.create_calc_tab()
        self.create_compare_hash_tab()
        self.create_compare_files_tab()

    def create_calc_tab(self):
        main_frame = ttk.Frame(self.tab_calc, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        algo_frame = ttk.LabelFrame(main_frame, text="选择哈希算法")
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm,
                                  values=SUPPORTED_ALGORITHMS,
                                  state='readonly', width=20)
        algo_combo.pack(padx=10, pady=10)

        file_frame = ttk.LabelFrame(main_frame, text="选择文件")
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(file_frame, textvariable=self.file_path_1, width=60).pack(
            side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="浏览", command=self.browse_file_1).pack(
            side=tk.RIGHT, padx=10, pady=10)

        result_frame = ttk.LabelFrame(main_frame, text="计算结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(result_frame, text="哈希值:").pack(anchor=tk.W, padx=10, pady=(10, 5))
        hash_entry = ttk.Entry(result_frame, textvariable=self.result_hash, width=100)
        hash_entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        hash_entry.config(state='readonly')

        copy_frame = ttk.Frame(result_frame)
        copy_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(copy_frame, text="复制哈希值", command=self.copy_hash).pack(side=tk.LEFT)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="计算哈希值", command=self.calculate_hash,
                   style='Accent.TButton').pack(pady=10)

    def create_compare_hash_tab(self):
        main_frame = ttk.Frame(self.tab_compare_hash, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        algo_frame = ttk.LabelFrame(main_frame, text="选择哈希算法")
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm,
                                  values=SUPPORTED_ALGORITHMS,
                                  state='readonly', width=20)
        algo_combo.pack(padx=10, pady=10)

        file_frame = ttk.LabelFrame(main_frame, text="选择文件")
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(file_frame, textvariable=self.file_path_1, width=60).pack(
            side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="浏览", command=self.browse_file_1).pack(
            side=tk.RIGHT, padx=10, pady=10)

        hash_input_frame = ttk.LabelFrame(main_frame, text="输入待比对的哈希值")
        hash_input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(hash_input_frame, textvariable=self.input_hash, width=100).pack(
            padx=10, pady=10, fill=tk.X)

        result_frame = ttk.LabelFrame(main_frame, text="比对结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.compare_hash_result_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.compare_hash_result_var,
                  font=('Arial', 12)).pack(padx=10, pady=20)

        self.compare_hash_icon_label = ttk.Label(result_frame)
        self.compare_hash_icon_label.pack(pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="开始比对", command=self.compare_with_hash,
                   style='Accent.TButton').pack(pady=10)

    def create_compare_files_tab(self):
        main_frame = ttk.Frame(self.tab_compare_files, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        algo_frame = ttk.LabelFrame(main_frame, text="选择哈希算法")
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm,
                                  values=SUPPORTED_ALGORITHMS,
                                  state='readonly', width=20)
        algo_combo.pack(padx=10, pady=10)

        file1_frame = ttk.LabelFrame(main_frame, text="文件一")
        file1_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(file1_frame, textvariable=self.file_path_1, width=60).pack(
            side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        ttk.Button(file1_frame, text="浏览", command=self.browse_file_1).pack(
            side=tk.RIGHT, padx=10, pady=10)

        file2_frame = ttk.LabelFrame(main_frame, text="文件二")
        file2_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(file2_frame, textvariable=self.file_path_2, width=60).pack(
            side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        ttk.Button(file2_frame, text="浏览", command=self.browse_file_2).pack(
            side=tk.RIGHT, padx=10, pady=10)

        hash_frame = ttk.LabelFrame(main_frame, text="哈希值")
        hash_frame.pack(fill=tk.X, pady=(0, 10))

        hash1_frame = ttk.Frame(hash_frame)
        hash1_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        ttk.Label(hash1_frame, text="文件一哈希:").pack(side=tk.LEFT)
        self.file1_hash_var = tk.StringVar()
        ttk.Label(hash1_frame, textvariable=self.file1_hash_var,
                  wraplength=700).pack(side=tk.LEFT, padx=10)

        hash2_frame = ttk.Frame(hash_frame)
        hash2_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        ttk.Label(hash2_frame, text="文件二哈希:").pack(side=tk.LEFT)
        self.file2_hash_var = tk.StringVar()
        ttk.Label(hash2_frame, textvariable=self.file2_hash_var,
                  wraplength=700).pack(side=tk.LEFT, padx=10)

        result_frame = ttk.LabelFrame(main_frame, text="检验结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.compare_files_result_var = tk.StringVar()
        ttk.Label(result_frame, textvariable=self.compare_files_result_var,
                  font=('Arial', 12)).pack(padx=10, pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(button_frame, text="开始检验", command=self.compare_files,
                   style='Accent.TButton').pack(pady=10)

    def browse_file_1(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.file_path_1.set(file_path)
            self.result_hash.set('')
            self.compare_hash_result_var.set('')
            self.file1_hash_var.set('')
            self.compare_files_result_var.set('')

    def browse_file_2(self):
        file_path = filedialog.askopenfilename(title="选择文件")
        if file_path:
            self.file_path_2.set(file_path)
            self.file2_hash_var.set('')
            self.compare_files_result_var.set('')

    def calculate_hash(self):
        file_path = self.file_path_1.get()
        if not file_path:
            messagebox.showwarning("警告", "请先选择文件")
            return

        try:
            hash_value = calculate_hash(file_path, self.algorithm.get())
            self.result_hash.set(hash_value)
        except Exception as e:
            messagebox.showerror("错误", f"计算哈希值失败: {str(e)}")

    def compare_with_hash(self):
        file_path = self.file_path_1.get()
        expected_hash = self.input_hash.get().strip()

        if not file_path:
            messagebox.showwarning("警告", "请先选择文件")
            return

        if not expected_hash:
            messagebox.showwarning("警告", "请输入待比对的哈希值")
            return

        try:
            actual_hash = calculate_hash(file_path, self.algorithm.get())
            self.result_hash.set(actual_hash)

            if compare_hashes(actual_hash, expected_hash):
                self.compare_hash_result_var.set("哈希值匹配！文件完整无误。")
            else:
                self.compare_hash_result_var.set("哈希值不匹配！文件可能已被篡改。")

        except Exception as e:
            messagebox.showerror("错误", f"比对失败: {str(e)}")

    def compare_files(self):
        file_path_1 = self.file_path_1.get()
        file_path_2 = self.file_path_2.get()

        if not file_path_1:
            messagebox.showwarning("警告", "请先选择文件一")
            return

        if not file_path_2:
            messagebox.showwarning("警告", "请先选择文件二")
            return

        try:
            hash1 = calculate_hash(file_path_1, self.algorithm.get())
            hash2 = calculate_hash(file_path_2, self.algorithm.get())

            self.file1_hash_var.set(hash1)
            self.file2_hash_var.set(hash2)

            if compare_hashes(hash1, hash2):
                self.compare_files_result_var.set("两个文件的哈希值相同，文件内容一致。")
            else:
                self.compare_files_result_var.set("两个文件的哈希值不同，文件内容不一致。")

        except Exception as e:
            messagebox.showerror("错误", f"检验失败: {str(e)}")

    def copy_hash(self):
        hash_value = self.result_hash.get()
        if hash_value:
            self.root.clipboard_clear()
            self.root.clipboard_append(hash_value)
            messagebox.showinfo("提示", "哈希值已复制到剪贴板")


def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = HashValidatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()