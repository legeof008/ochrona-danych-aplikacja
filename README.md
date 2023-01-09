# Wstęp do projektu 
Celem projektu jest utworzenie bezpiecznej aplikacji inernetowej pozwaljaącej zalogowanemu użyutkownikowi przechowywać jego hasła.
Użytwkonij jest identyfikowany przy pomocy swojego loginu i hasła. Ponadto zna on hasło główne pozwalające odszyfować hasła przechowywane w menadżerze.

Warto więc na samym początku ukazać relację pomiędzy danymi wyczytywanymi i walidowanymi przez aplikację.

![db_schema](https://user-images.githubusercontent.com/72550341/208308172-88c20c51-d098-45de-952c-17d4f84969cc.png)


# Zastosowane rozwiązania
## Rejestracja nowego użytkownika
Jako, że dane użytkownika będą wchodzić w interakcję z bazą danych, aplikacja będzie:
- akceptowała wyłącznie nazwę użytkownika spełniającą wybrane wyrażenie regularne,
- będzie akceptowała jedynie hasła o minimalnej długości 5 znaków, bez znaków białych,
- wszystkie zapytania do bazy danych będą prametryzowany aby zapobiec atakom sql injection
- nazwa użytkownika będzie filtrowana przeciw atakom JS injection.
## Autoryzacja użytkownika 
Z tych samych powodów autoryzacja użytkownika będze:
- akceptował wyłącznie nazwy użytkownika spełniające wyrażenie regularne, bez jawnego powiadamiania o niespełnieniu tego wymogu,
- akceptowała wyłącznie hasła o długości minimalnej 5 znaków oraz bez znaków białych, bez powiadamiania o niespełnieniu tego wymogu,
- wykonywałą zapytania paramteryzowane aby zapobiec sql injection,
- wykorzystywała technikę Double Submit Cookie :

![logging_in_protocol](https://user-images.githubusercontent.com/72550341/208308189-bd87ed34-6c24-4e43-8587-3daadf8f93cd.png)

- wymuszała maksymalną ilość prób logowania zarówno z danego użytkownika jak i z danego ip, potem kilkuminutowy 'cooldown'
- kontrolowała czy urządzenie użytkownika jest takie samo jak urządzenie z którego dokonywano rejestracji.
## Przechowywanie haseł 
Głównym założeniem jakie sobie obrałem było to, że żadna forma plaintextu nie powinna być trzymana w żadnej bazie danych. Zadecydowałem więc, że wykorzystam funkcję **PBKDF2** oraz **AES-256**.
Algorytm by wyglądał tak:
- generowaniego losowego salt i umieszczanie go w bazie danych,
- używając PBKDF2 z wysoką ilością iteracji generuję 640 bitową bazę na klucz,
- pierwsze 128 bitów będzię IV dla szyfru,
- kolejne 256 bitów będzie kluczem szyfru dla AES-256,
- ostatnie 256 bitów zostanie użytych do uwieżytelnienia szyfrowania.
```python
key = PBKDF2-SHA256(password, salt, 50000, 80)
iv = key[0:128]
cipherKey = key[128:384]
macKey = key[384:640]
```
![full_db_schema](https://user-images.githubusercontent.com/72550341/208316291-943b19dd-086e-496f-97cc-17f6977f133b.png)

Plusem takiego rozwiązania jest jednoznaczna uwierzytelnienia metodą "coś co wiem". Minusem jest brak innej metody aby zwiększyć skuteczność rozwiązania. Dodatkowo w przypadku zgubienia klucza (hasło nie będzie przechowywane w bazie danych ) dane przepadają.
## Rozwiązania technologiczne
Mimo iż nie chcę się jednoznacznie przywiązywać do jakiejkolwiek technologii, to na pewno wiem, że będę używał pythonowego **flask'a** oraz jego podpakietów zorientowanych pod poszczególne funkcjonalności jak np. **flask-login**,**flask-sql** etc. Jak w każdym projekcie, założenia projektu mogą ewoluować ze względu na ograniczenia techniczne, ja jednak wolałbym granicę teoretyczną pozostawić twardą, a techniczną nieco bardziej płynną.

# Roadmap funkcjonalności do zrobienia
- [x] w pełni bezpieczna rejestracja
- [x] w pełni bezpieczne logowanie
- [x] szyfrowanie haseł
- [ ] deszyfrowanie haseł
- [ ] zabezpieczenie timeout