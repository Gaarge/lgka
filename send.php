<?php
header('Content-Type: application/json; charset=utf-8');

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require __DIR__ . '/vendor/autoload.php';

$rawData = file_get_contents('php://input');
$data = json_decode($rawData, true);

$name = trim($data['name'] ?? '');
$phone = trim($data['phone'] ?? '');
$message = trim($data['message'] ?? '');

if ($name === '' || $phone === '') {
    http_response_code(400);
    echo json_encode([
        'ok' => false,
        'message' => 'Укажите имя и телефон.'
    ]);
    exit;
}

$mail = new PHPMailer(true);

try {
    // SMTP Gmail
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com';
    $mail->SMTPAuth = true;

    // Твоя Gmail-почта
    $mail->Username = 'vladram3707@gmail.com';

    // НЕ обычный пароль от Gmail, а пароль приложения Google
    $mail->Password = 'opvb ckvs uytg ltbb';

    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = 587;

    // От кого и кому
    $mail->setFrom('vladram3707@gmail.com', 'Сайт ЛГКА');
    $mail->addAddress('vladram4707@gmail.com');

    // Содержимое письма
    $mail->CharSet = 'UTF-8';
    $mail->Subject = 'Новая заявка с сайта ЛГКА';

    $mail->Body =
        "Новая заявка с сайта ЛГКА\n\n" .
        "Имя: {$name}\n" .
        "Телефон: {$phone}\n" .
        "Вопрос: " . ($message !== '' ? $message : 'Не указан') . "\n";

    $mail->send();

    echo json_encode([
        'ok' => true,
        'message' => 'Спасибо! Мы свяжемся с вами в ближайшее время.'
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'ok' => false,
        'message' => 'Не удалось отправить заявку.',
        'error' => $mail->ErrorInfo
    ]);
}
