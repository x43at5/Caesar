import unittest
import tkinter as tk
from tkinter import ttk
import _tkinter

def cipher(txt, shift):
    """Универсальная функция шифрования/дешифрования"""
    new_txt = ""
    m = ord("а")
    n = ord("я")
    M = ord("А")
    N = ord("Я")
    
    for s in txt:
        k = ord(s)
        
        if shift == 1:
            if (k>=m and k<n) or (k>=M and k<N):
                s = chr(k+1)
            elif k==n:
                s = chr(m)
            elif k==N:
                s = chr(M)
        else:
            if (k>m and k<=n) or (k>M and k<=N):
                s = chr(k-1)
            elif k==m:
                s = chr(n)
            elif k==M:
                s = chr(N)
        
        new_txt += s
    
    return new_txt


class CipherApp:
    """Упрощенная версия приложения для тестирования"""
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Цезаря")
        
        self.input_text = tk.Text(root, height=5, width=50)
        self.input_text.pack(pady=5)
        
        self.encrypt_btn = ttk.Button(root, text="Зашифровать", command=self.encrypt_text)
        self.encrypt_btn.pack()
        
        self.decrypt_btn = ttk.Button(root, text="Расшифровать", command=self.decrypt_text)
        self.decrypt_btn.pack()
        
        self.output_text = tk.Text(root, height=5, width=50)
        self.output_text.pack(pady=5)
    
    def encrypt_text(self):
        text = self.input_text.get("1.0", "end-1c")
        result = cipher(text, 1)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
    
    def decrypt_text(self):
        text = self.input_text.get("1.0", "end-1c")
        result = cipher(text, -1)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)


class TkinterTestCase(unittest.TestCase):
    """Базовый класс для тестирования Tkinter"""
    
    def setUp(self):
        """Создание окна перед каждым тестом"""
        self.root = tk.Tk()
        self.app = CipherApp(self.root)
        self.pump_events()
    
    def tearDown(self):
        """Закрытие окна после каждого теста"""
        if self.root:
            self.root.destroy()
            self.pump_events()
    
    def pump_events(self):
        """Обработка всех событий GUI"""
        while self.root.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
            pass


class TestCipherGUI(TkinterTestCase):
    
    def test_encrypt_button(self):
        """Тест кнопки шифрования"""
        # Вводим текст
        self.app.input_text.insert("1.0", "привет")
        self.pump_events()
        
        # Нажимаем кнопку шифрования
        self.app.encrypt_btn.invoke()
        self.pump_events()
        
        # Проверяем результат
        result = self.app.output_text.get("1.0", "end-1c")
        self.assertEqual(result, "рсйгжу")
    
    def test_decrypt_button(self):
        """Тест кнопки дешифрования"""
        # Вводим зашифрованный текст
        self.app.input_text.insert("1.0", "рсйгжу")
        self.pump_events()
        
        # Нажимаем кнопку дешифрования
        self.app.decrypt_btn.invoke()
        self.pump_events()
        
        # Проверяем результат
        result = self.app.output_text.get("1.0", "end-1c")
        self.assertEqual(result, "привет")
    
    def test_empty_input(self):
        """Тест с пустым вводом"""
        # Не вводим ничего
        self.app.encrypt_btn.invoke()
        self.pump_events()
        
        result = self.app.output_text.get("1.0", "end-1c")
        self.assertEqual(result, "")
    
    def test_roundtrip_through_gui(self):
        """Тест шифрования и дешифрования через GUI"""
        original = "тест"
        
        # Шифруем
        self.app.input_text.insert("1.0", original)
        self.pump_events()
        self.app.encrypt_btn.invoke()
        self.pump_events()
        
        # Копируем результат в input
        encrypted = self.app.output_text.get("1.0", "end-1c")
        self.app.input_text.delete("1.0", "end")
        self.app.input_text.insert("1.0", encrypted)
        self.pump_events()
        
        # Дешифруем
        self.app.decrypt_btn.invoke()
        self.pump_events()
        
        # Проверяем
        result = self.app.output_text.get("1.0", "end-1c")
        self.assertEqual(result, original)


if __name__ == '__main__':
    unittest.main()
