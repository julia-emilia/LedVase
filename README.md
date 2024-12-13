# LedVase
# Hardware
 * Der Microcontroller ist ein Raspberry Pico Pi 2. Er ist vielseitig einsetzbar und kann sowohl mit Python als auch C++ programmiert werden.
 * Der Led strip sind 93 WS2812 Leds. Diese werden mit 5 V versorgt und über ein serielles Protokoll angesteuert. In Python nutzt man das neopixel-Modul, um die Leds richtig anzusteuern.
 * Jede Led kann in 255 Stufen rot, grün und blau leuchten. Bei voller Helligkeit über längere Zeit könnten sich Bauteile erwärmen.
 * Ein USB-anschluss vom Laptop reicht aus, um alles zu versorgen. Soll es ohne Laptop leuchten, kann man das Netzeil nutzen.

# Software
 * Hier ist nur die Programmierung mit Python beschrieben.
 * Zur Programmierung nutze ich das Programm Thonny. Man kann es hier herunterladen: https://thonny.org/
 * Die folgende Anleitung bezieht sich auf Thonny 4.1.6
 * Ist bereits eine lauffähige Software auf dem Pico muss man ihn nur mit einem Micro-USB kabel an den Rechner anschließen. (Achtung bei manchen Ladekabeln fehlen die Datenleitungen)
 * Anschließend wählt man unten rechts unter Configure Interpreter "MicroPython (Raspberry Pi Pico) aus. Bei Port kann man "Try to detect Port automatically" auswählen.
 * Mit dem Knopf Run oder F5 kann man sein eigenes Programm starten.
 * Soll es automatisch auch ohne Rechner laufen, muss man unter File>Save copy und dann im Fenster "Save to Pi" auswählen. Die Datei muss main.py heißen.

# Was tun wenn beim Flashen etwas falsch lief?
 * Verbindet der Pi sich nicht mehr mit dem Rechner oder startet nicht mehr von selber, kann man ihn schnell komplett zurücksetzen.
 * Dafür muss man folgende Schritte befolgen:
   - Das USB Kabel und jede Versorgung abstecken.
   - Den Knopf auf dem Pi drücken und gedrückt halten
   - Das USB Kabel wieder einstecken
   - Jetzt den Knopf loslassen. Der Pi sollte wie ein USB-Stick erkannt werden.
   - In Thonny kann man nun wieder ins Configure Interpreter Menü gehen und auf "Install or Update MicroPython" drücken
   - Die Family ist "RP2", die Variant "Sparkfun Pico RP2040 PRO"
   - Ist das Installieren abgeschlossen, das USB kabel wieder abziehen und erneut an den Rechner stecken. Ab dann sollte Thonny den Pi wieder finden.

