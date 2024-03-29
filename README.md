# Wstęp do projektu 
Celem projektu jest utworzenie bezpiecznej aplikacji inernetowej pozwaljaącej zalogowanemu użyutkownikowi przechowywać jego hasła.
Użytwkonij jest identyfikowany przy pomocy swojego loginu i hasła. Ponadto zna on hasło główne pozwalające odszyfować hasła przechowywane w menadżerze.

Warto więc na samym początku ukazać relację pomiędzy danymi wyczytywanymi i walidowanymi przez aplikację.

![db_schema](https://user-images.githubusercontent.com/72550341/211797664-6d794ec1-814b-4a24-9292-1482500c1421.png)


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
key = PBKDF2-SHA256(password+username, salt, 50000, 80)
iv = key[0:128]
cipherKey = key[128:384]
macKey = key[384:640]
```

Hasła będą musiały być dodatkowo rozciągane do wielokrotności 16-stu ze względu na ograniczenia `AES`. Długość nonce'a będzie przechowywana w bazie danych.

Plusem takiego rozwiązania jest jednoznaczna uwierzytelnienia metodą "coś co wiem". Minusem jest brak innej metody aby zwiększyć skuteczność rozwiązania. Dodatkowo w przypadku zgubienia klucza (hasło nie będzie przechowywane w bazie danych ) dane przepadają.
## Komuniacja Sieciowa
Komunikacja między serwerem a klientem będzie szyfrowana tzn. przekazywana protokołem `https` w celu zachowania poufności nie tylko danych wymienianych kanałami poufnymi jak i by zabezpieczyć dodatkowo metodę `double submit cookie`.


## Rozwiązania technologiczne
Mimo iż nie chcę się jednoznacznie przywiązywać do jakiejkolwiek technologii, to na pewno wiem, że będę używał pythonowego **flask'a** oraz jego podpakietów zorientowanych pod poszczególne funkcjonalności jak np. **flask-login**,**flask-sqlalchemy** etc. Jak w każdym projekcie, założenia projektu mogą ewoluować ze względu na ograniczenia techniczne, ja jednak wolałbym granicę teoretyczną pozostawić twardą, a techniczną nieco bardziej płynną.
# Użycie
## Przygotowanie
Aplikacja została zdockeryzowana i korzysta z `docker-compose` w ramach gdyby nie był on dostępny należy zmienić linijkę w `Makefile` z:
```Makefile
DOCKER_COMPOSE=docker-compose
```
na:
```Makefile
DOCKER_COMPOSE=docker compose
```
## Skorzystanie z aplikacji
Aby uruchomić kontener należy użyć:
```
make start
```
Aby zatrzymać kontener należy użyć:
```
make stop
```
Aby usunąć niepotrzebne obrazy należy użyć:\
```
make clean
```
Aplikacja wykorzystuje port `8080` i włącznie przyjmuje zapytania protokołem `https`. Wykorzystywany jest podpisany przeze mnie certyfikat, więc komunikaty o niezaufanym połączeniu będą się pojawiały. Aplikacja dostępna powinna być pod adresem: 
```
https://localhost:8080/
```
Notatki zapisuje się w formie `Markdown`.
