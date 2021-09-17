#include "SoftwareSerial.h"
SoftwareSerial serial_connection(3, 4);
const int BUFFER_SIZE = 64;
#define LED A5
char inData[BUFFER_SIZE];
char inChar = 1;
int i = 0;

int Left_motor_go=8;     
int Left_motor_back=9;    

int Right_motor_go=6;   
int Right_motor_back=7;   

int Right_motor_en=5;  
int Left_motor_en=10; 

int Left_led=3;//Left led 
int Right_led=4;//Right led

int forward_speed = 129;
int even_out_speed = 59;
int left_turn_speed = 1650;
int right_turn_speed = 215;


void setup() {
  Serial.begin(9600);
  serial_connection.begin(9600);
  Serial.println("Ready!");
  pinMode(LED, OUTPUT);
  pinMode(Left_motor_go,OUTPUT); 
  pinMode(Right_motor_go,OUTPUT);
  pinMode(Right_motor_en,OUTPUT);
  pinMode(Left_motor_en,OUTPUT);
}


void run()     // ahead
{
  analogWrite(Left_motor_en, forward_speed - even_out_speed);
  analogWrite(Right_motor_en, forward_speed);
  digitalWrite(Left_motor_go, HIGH);
  digitalWrite(Right_motor_go, HIGH);
}

void left()        //turn left
{
  
  analogWrite(Right_motor_en, right_turn_speed);
  digitalWrite(Left_motor_go, LOW);
  digitalWrite(Right_motor_go, HIGH);
}

void right()      //turn right
{
  analogWrite(Left_motor_en, left_turn_speed);
    digitalWrite(Right_motor_go, LOW);
  digitalWrite(Left_motor_go, HIGH);
}

void brake()         //STOP
{
  
  digitalWrite(Right_motor_go,LOW);//Stop the right motor
  //digitalWrite(Right_motor_back,LOW);
  digitalWrite(Left_motor_go,LOW);//Stop the left motor
  //digitalWrite(Left_motor_back,LOW);
  //delay(time * 100);  //Running time can be adjusted 
  //led();
  
}

void loop() {
  byte byte_count = serial_connection.available();
  if (byte_count)
  {
    int first_bytes = byte_count;
    int remaining_bytes = 0;
    if (first_bytes >= (BUFFER_SIZE - 1))
    {
      remaining_bytes = byte_count - (BUFFER_SIZE - 1);
    }
    for (i = 0; i < first_bytes; i++)
    {
      inChar = serial_connection.read();
      inData[i] = inChar;
    }
    inData[i] = '\0';
    for (i = 0; i < remaining_bytes; i++)
    {
      inChar = serial_connection.read();
    }
    
    //Serial.println(inData);

    if (String(inData) == "F")
    {
      Serial.println("Going forward");
      run();
    }

    else if (String(inData) == "L")
    {
      Serial.println("Going left");
      left();
    }

    else if (String(inData) == "R")
    {
      Serial.println("Going right");
      right();
    }

    else if (String(inData) == "B")
    {
      Serial.println("Braking");
      brake();
    }

  }

  delay(1000/30);
}
