
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  // I2C LCD를 초기화 합니다..
  lcd.init();
  // I2C LCD의 백라이트를 켜줍니다.
  lcd.backlight();

}

String read_serial()
{
  String str = "";

  while( Serial.available()){char ch = Serial.read();   str.concat(ch);} 
  return str;
}

void loop() {
  String str = read_serial();
  //Serial.println("hello");
  if(str.length()>0){
    lcd.clear();
    lcd.setCursor(0,0);           // 0번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.println(str);
    if(str.length()>16){
      String s2 = "";
      for(int i=16;i<str.length();i++)s2+=str[i];
      lcd.setCursor(0,1);           // 0번째 줄 0번째 셀부터 입력하게 합니다.
      lcd.println(s2);
    }
  }
  delay(1000);
  // LCD의 모든 내용을 삭제합니다.

}
