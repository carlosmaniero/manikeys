// Definition of the buzzer pin (A1)
const int buzzerPin = A1;

// Definition of musical note frequencies (in Hz)
const int note_G4 = 392; // G4
const int note_D5 = 587; // D5 (High)
const int note_E4 = 330; // E4 (Low)
const int note_B4 = 494; // B4

// Timing variables (in milliseconds)
int noteDuration = 5;        // Initial snappier duration
const int breakDuration = 10;   // Crisp break between notes

void setup() {
  // Configure pin A1 as an output
  pinMode(buzzerPin, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);

  // Run the startup sequence once
  for (int i = 0; i < 20; i++) {
    playNote(note_G4 * 1.22 * (i + 1), noteDuration);
  }

  noteDuration *= 2;

  for (int i = 20; i > 0 ; i-=2) {
    playNote(note_G4 * 1.22 * (i + 1), noteDuration);
  }

  digitalWrite(4, LOW);
}

void loop() {
  // Left empty so it only plays once at boot
}

// Custom function to handle playing a note, waiting, and inserting the break
void playNote(int noteFrequency, int duration) {
  tone(buzzerPin, noteFrequency);
  delay(duration);
  noTone(buzzerPin);
  delay(breakDuration);
}