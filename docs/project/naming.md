# Nazwa projektu i identyfikatory

Kanoniczna nazwa produktu to **Avatar Studio**. Nazwa produktu, repozytorium i publicznej dokumentacji została ujednolicona, natomiast identyfikatory techniczne zachowują formę właściwą dla danego ekosystemu.

## Konwencja nazw

| Kontekst | Nazwa |
| --- | --- |
| Produkt i dokumentacja | `Avatar Studio` |
| Repozytorium GitHub | `MatPomGit/avatar-studio` |
| Publiczna dokumentacja | `https://matpomgit.github.io/avatar-studio/` |
| Pakiet/import Python | `avatar_studio` |
| Nazwa dystrybucji Python | `avatar-studio` |
| Komenda CLI | `avatar-studio` |
| Katalog aplikacji | `apps/avatar_studio/` |
| Plik wykonywalny Windows | `AvatarStudio.exe` |
| Plik wykonywalny Linux | `AvatarStudio` |
| Katalog danych użytkownika | `.avatar-studio/` |

Nazwy modułów, pakietów, funkcji i zmiennych Python stosują PEP 8 i `snake_case`. Nazwa dystrybucji używa formy z łącznikiem zgodnej z normalizacją nazw pakietów Python.

## Nazwa repozytorium nie jest nazwą artefaktu

Nazwa katalogu sklonowanego repozytorium nie może być częścią kontraktu technicznego potoku. Użytkownik może sklonować projekt do dowolnego katalogu, dlatego skrypty nie powinny zakładać, że bieżący folder nazywa się `avatar-studio`.

Ta sama zasada dotyczy projektów narzędzi zewnętrznych. Przykładowo plik Unreal Engine `.uproject` może mieć niezależną nazwę. Adapter powinien otrzymać jego ścieżkę albo wykryć go na podstawie zawartości wskazanego katalogu.

## Zasada dla adresów URL

Adres repozytorium i publicznej dokumentacji są częścią konfiguracji produktu. Nie należy duplikować ich w wielu miejscach bez potrzeby. Jeśli aplikacja musi używać stałego adresu bazowego, powinien być zdefiniowany w jednym miejscu w danym module albo w konfiguracji.

## Kontrola regresji

CI sprawdza, czy usunięty identyfikator poprzedniego repozytorium nie został ponownie wprowadzony do aktywnych plików źródłowych, dokumentacji lub konfiguracji. Historyczne informacje o migracji należy opisywać bez przywracania starego identyfikatora jako aktywnej nazwy technicznej.
