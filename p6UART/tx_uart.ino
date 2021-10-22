// MCK 21MHz
void _sw_uart_wait_half_T() {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T() {
  _sw_uart_wait_half_T();
  _sw_uart_wait_half_T();
}

void setup() {
  pinMode(4,OUTPUT);
}


void loop() {
  digitalWrite(4,HIGH);
 _sw_uart_wait_T();


  //startbit
  digitalWrite(4,LOW);
 _sw_uart_wait_T();

  //envio do caracter t (01110100)
  digitalWrite(4,LOW);
 _sw_uart_wait_T();
  digitalWrite(4,LOW);
 _sw_uart_wait_T();
   digitalWrite(4,HIGH);
 _sw_uart_wait_T();
  digitalWrite(4,LOW);
 _sw_uart_wait_T();
  digitalWrite(4,HIGH);
 _sw_uart_wait_T();
  digitalWrite(4,HIGH);
 _sw_uart_wait_T();
  digitalWrite(4,HIGH);
 _sw_uart_wait_T();
  digitalWrite(4,LOW);
 _sw_uart_wait_T();

  //paridade  
  digitalWrite(4,LOW);
 _sw_uart_wait_T();

  //stopbit
  digitalWrite(4,HIGH);
 _sw_uart_wait_T();

 delay(3000);

}
