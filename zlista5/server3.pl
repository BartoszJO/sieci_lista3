use HTTP::Daemon;  # Załadowanie modułu HTTP::Daemon, który umożliwia tworzenie prostego serwera HTTP.
use HTTP::Status;  # Załadowanie modułu HTTP::Status, który zawiera stałe dla kodów statusu HTTP.
#use IO::File;     # (zakomentowane) Moduł IO::File, który mógłby być używany do operacji na plikach.

# Tworzenie nowego obiektu HTTP::Daemon, który nasłuchuje na localhost i porcie 4321.
my $d = HTTP::Daemon->new(
         LocalAddr => 'localhost',  # Adres lokalny, na którym serwer będzie nasłuchiwał.
         LocalPort => 4321,        # Port, na którym serwer będzie nasłuchiwał.
     ) || die;  # Jeśli nie uda się utworzyć serwera, program zakończy działanie z komunikatem błędu.

# Wyświetlenie w konsoli adresu URL, pod którym serwer jest dostępny.
print "Please contact me at: <URL:", $d->url, ">\n";

# Główna pętla serwera, która akceptuje połączenia od klientów.
while (my $c = $d->accept) {
    # Pętla obsługująca żądania HTTP od klienta.
    while (my $r = $c->get_request) {
        # Sprawdzenie, czy metoda HTTP użyta w żądaniu to GET.
        if ($r->method eq 'GET') {
            # Ścieżka do pliku, który zostanie wysłany jako odpowiedź (np. index.html).
            $file_s = "./index.html";  # index.html - plik, który musi istnieć w katalogu roboczym.
            $c->send_file_response($file_s);  # Wysłanie pliku jako odpowiedzi na żądanie.
        }
        else {
            # Jeśli metoda HTTP nie jest GET, zwrócenie błędu 403 (Forbidden).
            $c->send_error(RC_FORBIDDEN);
        }
    }
    # Zamknięcie połączenia z klientem.
    $c->close;
    undef($c);  # Zwolnienie zasobów związanych z połączeniem.
}
