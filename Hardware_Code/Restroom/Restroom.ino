int IR_k = 2;
int IR_l = 3;
float piezo_val;
bool count = false;

void setup()
{
  Serial.begin(9600);
}

void loop()
{  
  if (digitalRead(IR_k) ==  LOW && digitalRead(IR_l) == LOW)
  {
    count = !count;
  }

  if (count == false)
  {
    Serial.println("*");
  }

  if (count == true)
  {
    Serial.print('x');
    Serial.println(analogRead(A7));
  }
  delay(700);
}

