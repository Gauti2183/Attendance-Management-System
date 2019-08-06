#include <ESP8266WiFi.h>      // 提供Wi-Fi功能的程式庫
#include <ESP8266WebServer.h>  // 提供網站伺服器功能的程式庫
#define SS_PIN 4  //D2
#define RST_PIN 5 //D1

#include <SPI.h>
#include <MFRC522.h>

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

const char ssid[] = "uhong_ap";
const char pass[] = "0952474239s";
const int buzzer = 10;
const int ledlight = 9;

String content= "";

char member[101] ;
ESP8266WebServer server(80);   // 宣告網站伺服器物件與埠號

// 定義處理首頁請求的自訂函式
void rootRouter() {
  server.send(200, "text/html", member);   //網頁的html 在此(紅色字體可做修改)
  
}

void setup() {
  DataReset();
  Serial.begin(115200);  
  WiFi.begin(ssid, pass);
  SPI.begin();      // Initiate  SPI bus
  pinMode(buzzer, OUTPUT);
  pinMode(ledlight, OUTPUT);
  digitalWrite(ledlight,LOW);
  noTone(buzzer);
  mfrc522.PCD_Init();   // Initiate MFRC522

  /*
   *  若要指定IP位址，請自行在此加入WiFi.config()敘述。
   WiFi.config(IPAddress(192,168,1,50),    // IP位址
               IPAddress(192,168,1,1),     // 閘道（gateway）位址
               IPAddress(255,255,255,0));  // 網路遮罩（netmask）
   */

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);   // 等待WiFi連線
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected, IP: ");
  Serial.println(WiFi.localIP());  // 顯示ESP8266裝置的IP位址

  server.on("/index.html", rootRouter);  // 處理首頁連結請求的事件
  server.on("/", rootRouter);
  
  server.onNotFound([](){   // 處理「找不到指定路徑」的事件
    server.send(404, "text/plain", "File NOT found!");
  });
  
  server.begin();
  Serial.println("HTTP server started.");
}

void loop() {


    server.handleClient();  // 處理用戶連線

if (server.client() != 0)
{
  DataReset();
  Serial.println("data get and reset");
}
    // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  buzz();
  //Show UID on serial monitor
  Serial.println();
  Serial.print(" UID tag :");
  
  byte letter;
  content = " ";
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : "");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : ""));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  if ((content.substring(1) == "F51D19DA") && (member[0] != '1')) member[0] = '1';
  if (content.substring(1) == "65E5EF2E" && (member[1] != '1')) member[1] = '1';
  if (content.substring(1) == "46C592D7" && (member[2] != '1')) member[2] = '1';
  if (content.substring(1) == "76B08CD7" && (member[3] != '1')) member[3] = '1';
  if (content.substring(1) == "568C8FD7" && (member[4] != '1')) member[4] = '1';
  if (content.substring(1) == "661390D7" && (member[5] != '1')) member[5] = '1';
  if (content.substring(1) == "F64294D7" && (member[6] != '1')) member[6] = '1';
  if (content.substring(1) == "762393D7" && (member[7] != '1')) member[7] = '1';
  if (content.substring(1) == "C6B48ED7" && (member[8] != '1')) member[8] = '1';
  if (content.substring(1) == "963390D7" && (member[9] != '1')) member[9] = '1';
  if (content.substring(1) == "868AA3DB" && (member[10] != '1')) member[10] = '1';
  if (content.substring(1) == "B6EFE4DA" && (member[11] != '1')) member[11] = '1';
  if (content.substring(1) == "36C2E5DA" && (member[12] != '1')) member[12] = '1';
  if (content.substring(1) == " 06 0FFEDB" && (member[13] != '1')) member[13] = '1';
  if (content.substring(1) == "2522C7DC" && (member[14] != '1')) member[14] = '1';
    
  Serial.println();
  Serial.println(member);
}

void DataReset(){
    for (int i=0 ;i<101; i++){
  member[i] = '0';
  }
}
void buzz(){
  tone(buzzer, 3000);
  digitalWrite(ledlight,HIGH);
  delay(150);        
  noTone(buzzer);
  digitalWrite(ledlight,LOW);
  delay(50);  
  tone(buzzer, 3000);
  digitalWrite(ledlight,HIGH);
  delay(150);
  noTone(buzzer); 
  digitalWrite(ledlight,LOW);
  delay(1500);
}
