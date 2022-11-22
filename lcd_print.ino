/*
 제목    : I2C LCD에 문자 출력하기
 내용   : I2C LCD에 원하는 문자를 표시해 봅니다.  
 */

// LCD를 쉽게 제어하기 위한 라이브러리를 추가합니다.
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// 0x3F I2C 주소를 가지고 있는 16x2 LCD객체를 생성합니다.(I2C 주소는 LCD에 맞게 수정해야 합니다.)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// 실행시 가장 먼저 호출되는 함수이며, 최초 1회만 실행됩니다.
// 변수를 선언하거나 초기화를 위한 코드를 포함합니다.
void setup() {
  // I2C LCD를 초기화 합니다..
  lcd.init();
  // I2C LCD의 백라이트를 켜줍니다.
  lcd.backlight();
}

// setup() 함수가 호출된 이후, loop() 함수가 호출되며,
// 블록 안의 코드를 무한히 반복 실행됩니다.
void loop() { 
  // random 함수를 사용하여 0부터 2까지의 숫자중 랜덤하게 값을 받습니다.
  int value = random(0, 3);
  // 랜덤 값이 0이라면 아래의 조건을 실행합니다.
  if (value == 0) {//sadasds
    // 0번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.setCursor(0,0);           // 0번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.print("  KocoaFab.cc  ");       // 문구를 출력합니다.
  }
  // 랜덤 값이 1이라면 아래의 조건을 실행합니다.
  else if (value == 1) {
    lcd.setCursor(0,1);           // 1번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.print("  Hello World!!  ");     // 문구를 출력합니다.
  }
  // 랜덤 값이 2이라면 아래의 조건을 실행합니다.
  else if (value == 2) {
    // 0번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.setCursor(0,0);
    // 아래의 문장을 출력합니다.
    lcd.print("  KocoaFab.cc  ");
    // 1번째 줄 0번째 셀부터 입력하게 합니다.
    lcd.setCursor(0,1);
    // 아래의 문장을 출력합니다.
    lcd.print("  Hello World!!  ");
  }
  // 1초간 대기합니다.
  delay(1000);
  // LCD의 모든 내용을 삭제합니다.
  lcd.clear();
}
