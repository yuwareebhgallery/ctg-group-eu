<?php
// view.php

// Pfad zur PDF-Datei
$pdfFile = 'leistungsverzeichnis.pdf';

// Pfad zur Log-Datei für Ansicht
$logFile = 'views.log';

// Prüfen, ob die Datei existiert
if (!file_exists($pdfFile)) {
    header("HTTP/1.0 404 Not Found");
    exit("Datei nicht gefunden.");
}

// Ansicht protokollieren
$date   = date('Y-m-d H:i:s');
$ip     = $_SERVER['REMOTE_ADDR'];
$agent  = $_SERVER['HTTP_USER_AGENT'];
$logLine = "$date\t$ip\t$agent\n";

file_put_contents($logFile, $logLine, FILE_APPEND);

// PDF inline im Browser anzeigen
header('Content-Type: application/pdf');
header('Content-Disposition: inline; filename="' . basename($pdfFile) . '"');
header('Content-Length: ' . filesize($pdfFile));

readfile($pdfFile);
exit;
?>
