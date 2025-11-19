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


def test_encrypt_simple():
    """Простой тест шифрования"""
    assert cipher("привет", 1) == "рсйгжу"

def test_decrypt_simple():
    """Простой тест дешифрования"""
    assert cipher("рсйгжу", -1) == "привет"

def test_roundtrip():
    """Тест обратимости"""
    original = "тестовое сообщение"
    encrypted = cipher(original, 1)
    decrypted = cipher(encrypted, -1)
    assert original == decrypted

def test_last_letter():
    """Тест последней буквы алфавита"""
    assert cipher("я", 1) == "а"

def test_first_letter():
    """Тест первой буквы алфавита"""
    assert cipher("а", -1) == "я"

def test_empty_string():
    """Тест пустой строки"""
    assert cipher("", 1) == ""

def test_numbers_and_symbols():
    """Тест что цифры и символы не изменяются"""
    assert cipher("123!@#", 1) == "123!@#"
