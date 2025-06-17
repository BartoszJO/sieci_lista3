use HTTP::Daemon; # Załadowanie modułu HTTP::Daemon do obsługi serwera HTTP.
use HTTP::Status; # Załadowanie modułu HTTP::Status do obsługi kodów statusu HTTP.

# Tworzenie nowego obiektu serwera HTTP na lokalnym adresie i porcie 4321.
my $daemon = HTTP::Daemon->new(
    LocalAddr => "localhost", # Adres lokalny, na którym serwer będzie nasłuchiwał.
    LocalPort => 4321,        # Port lokalny, na którym serwer będzie nasłuchiwał.
) || die; # Jeśli nie uda się utworzyć serwera, zakończ program.

# Wyświetlenie adresu URL, pod którym działa serwer.
print "Running at: ", $daemon->url, "\n";

# Główna pętla serwera, która akceptuje połączenia.
while (my $connection = $daemon->accept) {
    # Obsługa żądań w ramach jednego połączenia.
    while (my $request = $connection->get_request) {
        # Sprawdzenie, czy metoda żądania to GET.
        if ($request->method ne "GET") {
            # Jeśli metoda nie jest GET, zwróć błąd 403 (Forbidden).
            $connection->send_error(RC_FORBIDDEN);
            next; # Przejdź do następnego żądania.
        }

        # Pobranie URI z żądania.
        my $uri = $request->uri;
        # Jeśli ścieżka URI to "/header", zwróć nagłówki żądania.
        if ($uri->path eq "/header") {
            my $headers = $request->headers_as_string; # Pobranie nagłówków jako ciąg tekstowy.
            my $response = HTTP::Response->new(200); # Utworzenie odpowiedzi z kodem 200 (OK).
            $response->header("Content-Type" => "text/plain"); # Ustawienie typu treści na tekst zwykły.
            $response->content("Your request's header is:\n\n" . $headers); # Ustawienie treści odpowiedzi.
            $connection->send_response($response); # Wysłanie odpowiedzi do klienta.
        } else {
            # Obsługa innych ścieżek URI.
            my $filename = $uri->path eq "/" ? "websites/index.html" : "websites" . $uri . ".html"; 
            # Jeśli ścieżka to "/", zwróć plik "index.html", w przeciwnym razie zwróć plik odpowiadający ścieżce.
            $connection->send_file_response($filename); # Wysłanie pliku jako odpowiedzi.
        }
    }

    # Zamknięcie połączenia po obsłużeniu wszystkich żądań.
    $connection->close;
    undef($connection); # Zwolnienie zasobów połączenia.
}