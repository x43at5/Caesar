import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

def encrypt_text():
    """Шифрование текста"""
    text = text_field.get("1.0", "end-1c")
    if not text.strip():
        status_label.config(text="⚠ Введите текст", foreground="#e74c3c")
        return
    
    result = cipher(text, 1)
    text_field.delete("1.0", "end")
    text_field.insert("1.0", result)
    
    encrypt_btn.config(state='disabled')
    decrypt_btn.config(state='normal')
    copy_btn.config(state='normal')
    status_label.config(text="✓ Зашифровано", foreground="#27ae60")

def decrypt_text():
    """Дешифрование текста"""
    text = text_field.get("1.0", "end-1c")
    if not text.strip():
        status_label.config(text="⚠ Введите текст", foreground="#e74c3c")
        return
    
    result = cipher(text, -1)
    text_field.delete("1.0", "end")
    text_field.insert("1.0", result)
    
    decrypt_btn.config(state='disabled')
    encrypt_btn.config(state='normal')
    copy_btn.config(state='normal')
    status_label.config(text="✓ Расшифровано", foreground="#3498db")

def copy_to_clipboard():
    """Копирование текста в буфер обмена"""
    text = text_field.get("1.0", "end-1c")
    if not text.strip():
        status_label.config(text="⚠ Нечего копировать", foreground="#e74c3c")
        return
    
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        status_label.config(text="✓ Скопировано", foreground="#9b59b6")
    except Exception as e:
        status_label.config(text="⚠ Ошибка", foreground="#e74c3c")

def clear_text():
    """Очистка поля и сброс состояния"""
    if text_field.get("1.0", "end-1c").strip():
        result = messagebox.askyesno("Подтверждение", "Очистить текст?")
        if not result:
            return
    
    text_field.delete("1.0", "end")
    encrypt_btn.config(state='normal')
    decrypt_btn.config(state='disabled')
    copy_btn.config(state='disabled')
    status_label.config(text="Готов", foreground="#95a5a6")

def on_text_change(event):
    """Обработчик изменения текста"""
    if event.keysym not in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R']:
        text = text_field.get("1.0", "end-1c")
        encrypt_btn.config(state='normal')
        decrypt_btn.config(state='normal')
        copy_btn.config(state='normal' if text.strip() else 'disabled')
        status_label.config(text="Изменён", foreground="#f39c12")

def handle_ctrl_keys(event):
    """Обработчик Ctrl комбинаций"""
    if event.state & 0x4:
        if event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
            return "break"
        elif event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
            root.after(10, lambda: on_text_change(event))
            return "break"
        elif event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
            return "break"
        elif event.keycode == 65:
            event.widget.tag_add("sel", "1.0", "end")
            event.widget.mark_set("insert", "1.0")
            event.widget.see("insert")
            return "break"
    root.after(1, lambda: on_text_change(event))

def make_context_menu(widget):
    """Создание контекстного меню"""
    context_menu = tk.Menu(widget, tearoff=0)
    context_menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.add_separator()
    context_menu.add_command(label="Выделить всё", command=lambda: select_all(widget))
    
    def show_context_menu(event):
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    widget.bind("<Button-3>", show_context_menu)

def select_all(widget):
    """Выделить весь текст"""
    widget.tag_add("sel", "1.0", "end")
    widget.mark_set("insert", "1.0")
    widget.see("insert")
    return "break"

# Создание окна
root = tk.Tk()
root.title("Шифр Цезаря")
root.geometry("620x450")
root.minsize(480, 380)  # Минимальный размер для всех элементов

# Применяем тему
style = ttk.Style()
available_themes = style.theme_names()
if 'vista' in available_themes:
    style.theme_use('vista')
elif 'winnative' in available_themes:
    style.theme_use('winnative')
elif 'clam' in available_themes:
    style.theme_use('clam')

# Темная цветовая схема
bg_color = "#2c3e50"
root.configure(bg=bg_color)

# Настройка стилей
style.configure('Dark.TFrame', background=bg_color)
style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), padding=(12, 10))
style.configure('Secondary.TButton', font=('Segoe UI', 10), padding=(12, 10))
style.configure('Copy.TButton', font=('Segoe UI', 10), padding=(12, 10))

# Главный контейнер с grid для лучшей адаптивности
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding="15", style='Dark.TFrame')
main_frame.grid(row=0, column=0, sticky="nsew")

# Настройка grid для main_frame - текстовое поле растягивается
main_frame.grid_rowconfigure(1, weight=1)  # Строка с текстовым полем
main_frame.grid_columnconfigure(0, weight=1)

# Заголовок (row 0)
title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
title_frame.grid_columnconfigure(0, weight=1)

title_label = ttk.Label(
    title_frame,
    text="🔐 Шифр Цезаря",
    background=bg_color,
    foreground="#ecf0f1",
    font=('Segoe UI', 18, 'bold')
)
title_label.grid(row=0, column=0, sticky="w")

status_label = ttk.Label(
    title_frame,
    text="Готов",
    foreground="#95a5a6",
    background=bg_color,
    font=("Segoe UI", 9)
)
status_label.grid(row=0, column=1, sticky="e", padx=(10, 0))

# Текстовое поле (row 1) - основной элемент, который растягивается
text_field = tk.Text(
    main_frame,
    font=("Segoe UI", 11),
    wrap=tk.WORD,
    relief=tk.FLAT,
    borderwidth=0,
    padx=12,
    pady=12,
    bg="#34495e",
    fg="#ecf0f1",
    insertbackground="#ecf0f1",
    selectbackground="#3498db",
    selectforeground="#ffffff",
    highlightthickness=2,
    highlightcolor="#3498db",
    highlightbackground="#34495e"
)
text_field.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
make_context_menu(text_field)
text_field.bind("<Key>", handle_ctrl_keys)

# Кнопки (row 2) - фиксированная высота
button_container = ttk.Frame(main_frame, style='Dark.TFrame')
button_container.grid(row=2, column=0, sticky="ew")
button_container.grid_columnconfigure((0, 1, 2), weight=1)

# Первая строка кнопок
encrypt_btn = ttk.Button(
    button_container,
    text="🔒 Зашифровать",
    command=encrypt_text,
    style='Primary.TButton'
)
encrypt_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

decrypt_btn = ttk.Button(
    button_container,
    text="🔓 Расшифровать",
    command=decrypt_text,
    state='disabled',
    style='Primary.TButton'
)
decrypt_btn.grid(row=0, column=1, sticky="ew", padx=(0, 5))

clear_btn = ttk.Button(
    button_container,
    text="🗑️ Очистить",
    command=clear_text,
    style='Secondary.TButton'
)
clear_btn.grid(row=0, column=2, sticky="ew")

# Вторая строка - кнопка копирования
copy_btn = ttk.Button(
    button_container,
    text="📋 Скопировать",
    command=copy_to_clipboard,
    state='disabled',
    style='Copy.TButton'
)
copy_btn.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 0))

# Запуск приложения
root.mainloop()
