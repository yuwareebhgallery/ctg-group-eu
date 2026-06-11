<?php
// download.php

// Pfad zur PDF-Datei
$pdfFile = 'leistungsverzeichnis.pdf';

// Pfad zur Log-Datei (stellen Sie sicher, dass diese beschreibbar ist)
$logFile = 'downloads.log';

// Prüfe, ob die Datei existiert
if (!file_exists($pdfFile)) {
    header("HTTP/1.0 404 Not Found");
    exit("Datei nicht gefunden.");
}

// Download-Event protokollieren
$date   = date('Y-m-d H:i:s');
$ip     = $_SERVER['REMOTE_ADDR'];
$agent  = $_SERVER['HTTP_USER_AGENT'];
$logLine = "$date\t$ip\t$agent\n";

// Logeintrag an die Log-Datei anhängen
file_put_contents($logFile, $logLine, FILE_APPEND);

// Header setzen, um den Download zu erzwingen
header('Content-Type: application/pdf');
header('Content-Disposition: attachment; filename="' . basename($pdfFile) . '"');
header('Content-Length: ' . filesize($pdfFile));

// PDF-Datei ausgeben
readfile($pdfFile);
exit;
?>
