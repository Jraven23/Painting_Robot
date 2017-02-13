/*
    Pins Interrupciones en Mega: --- INT 0, INT 1, INT 2, INT 3, INT 4, INT 5  --- 2, 3, 21,  20,  19,  18 ---
*/

int CH1=18;
int CH2=19;
int i=0;
int N_Lados;
int Radio;
int contador1=0;
int contador2;
void setup() {
  Serial.begin(115200);
  pinMode(CH1,INPUT);
  pinMode(CH2,INPUT);
  attachInterrupt( 5, CHANNEL1, CHANGE);
  attachInterrupt( 4, CHANNEL2, CHANGE);
  //attachInterrupt( 3, CHANNEL3, CHANGE);
  //attachInterrupt( 2, CHANNEL4, CHANGE);
 /*  while (i<2){
    if (i==0){
      if(Serial.available()>0){
        N_Lados = Serial.read();
       Serial.end();
       Serial.begin(9600);
        i++;
      }
    }
 
     if (i==1){
      if(Serial.available()>0){
        Radio = Serial.read();
        i++;
        Serial.print(N_Lados);
        Serial.println(Radio);
        i=0;
       }
     }    
  }*/
 
}

void loop() {

 //Comunicacion de movil con Arduino
  while(Serial.available()){
    if(Serial.read()==1){
      contador1=0;
      contador2=0;
    }
  }
}


void CHANNEL1(){
  Serial.print (++contador1);
 }
void CHANNEL2(){
  Serial.print (++contador1);
 }

/*void CHANNEL3(){
//  contador2++;
  Serial.print (contador2);
 }
//void CHANNEL4(){
  contador2++;
  Serial.print (contador2);
 }*/
