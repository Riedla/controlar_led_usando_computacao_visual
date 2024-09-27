int ledPin = 13;  // O pino onde o LED está conectado

void setup() {
  // Inicializa a comunicação serial a 9600 baud rate
  Serial.begin(9600);

  // Configura o pino do LED como saída
  pinMode(ledPin, OUTPUT);

  // Desliga o LED inicialmente
  digitalWrite(ledPin, LOW);
}

void loop() {
  // Verifica se existe algum dado disponível para leitura na comunicação serial
  if (Serial.available() > 0) {
    // Lê a string enviada via comunicação serial
    String command = Serial.readStringUntil('\n');

    // Remove espaços extras e quebras de linha
    command.trim();

    // Verifica se o comando é "ON"
    if (command == "ON") {
      digitalWrite(ledPin, HIGH);  // Liga o LED
      Serial.println("LED ligado");
    }

    // Verifica se o comando é "OFF"
    else if (command == "OFF") {
      digitalWrite(ledPin, LOW);  // Desliga o LED
      Serial.println("LED desligado");
    }
  }
}





