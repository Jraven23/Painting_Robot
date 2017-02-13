import RPi.GPIO as GPIO
import math
import serial
import time
from datetime import datetime
PI=3.14159265359
Alpha1=-40.0
Alpha2=40.0
d=5.0
L=11.0
l=9.0
sigmaq1=-1
sigmaq2=1
X_centro=0.0
Y_centro=11.25
Arduino1=serial.Serial('/dev/ttyACM0',57600)
Arduino2=serial.Serial('/dev/ttyACM1',57600)
N_pulsos1=3300
N_pulsos2=4741
Dif_grados1=360.0/N_pulsos1
Dif_grados2=360.0/N_pulsos2
PIN_Fin1=18
PIN_Fin2=17
PIN_ACT=22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_Fin1,GPIO.IN)
GPIO.setup(PIN_Fin2,GPIO.IN)
GPIO.setup(PIN_ACT,GPIO.OUT)
Calibrado=False
Calibrado1=False
Calibrado2=False
MODO='ARRANQUE'


class Punto:
        def __init__(self):#constructor
                self.x=0
                self.y=0
        def valor(self,x,y): #asignacion de valores
                self.x=x
                self.y=y
        def next_punto(self,vector,central_p): #pasa de vector a coord de punto
                self.x=vector.x+central_p.x
                self.y=vector.y+central_p.y
class Vector2D:
        def __init__(self, punto1, punto2): #constructor
                self.x=punto2.x-punto1.x
                self.y=punto2.y-punto1.y
        def giro(self,angle): #giro del vector cierto angulo
                x=self.x
                y=self.y
                self.x=x*math.cos(angle)-y*math.sin(angle)
                self.y=x*math.sin(angle)+y*math.cos(angle)

def Leer_Alpha1():
	pul=Arduino1.read(1)
	if pul=='-':
		pul=-int(Arduino1.read(1))
	else: 
		pul=int(pul)

	return (pul*Dif_grados1)
	
def Leer_Alpha2():
	pul=Arduino2.read(1)
	if pul=='-':
		pul=-int(Arduino2.read(1))
	else: 
		pul=int(pul)

	return (pul*Dif_grados2)

def CinDirecta(q1,q2):
	q1=math.radians(q1)
	q2=math.radians(q2)
	xd=-d/2 + l*math.cos(q2)
	yd=l*math.sin(q2)
	xb=d/2 +l*math.cos(q1)
	yb=l*math.sin(q1)
	A=-0.5*(xd*xd+yd*yd-xb*xb-yb*yb) #No anhado el -ldp+lbp pues siempre sera cero
	B=((yb-yd)*(yb-yd))*((xd*xd + yd*yd-L*L))+A*A -2*yd*(yb-yd)*A  #no pongo el termino Ldp y Lbp pues su resta es 0
	C=(yb-yd)*(yb-yd) + (xb-xd)*(xb-xd)
	D=2*yd*((yb-yd)*(xb-xd)) - 2*xd*((yb-yd)*(yb-yd))-2*A*(xb-xd)
	discriminante=math.sqrt(D*D-4*B*C) #La raiz de d al cuadrado - 4bc
	xp=((-D+discriminante)/(2*C))
	yp=(A-xp*(xb-xd))/(yb-yd)
	return [xp,yp]

def Vertices():
	for n in range(n_lados+1):
       		punto.append(Punto())
        	if n==0:
        		punto[n].valor(X_centro,Y_centro+Radio)
        		print "El punto ",n+1," es: ", punto[n].x,",",punto[n].y
                	vector0=Vector2D(punto0,punto[n]) #vector entre puntos
                	#print "El vector es: ",vector0.x,",",vector0.y
		else:
			if n==n_lados:
				punto[n]=punto[0]
			else:
				vector0.giro(alfarad) #giro del vector
       				#print "Vector girado: ",vector0.x,",",vector0.y
              			punto[n].next_punto(vector0,punto0) #calculo sig. punto
               		if punto[n].x<0.0005 and punto[n].x>-0.0005: punto[n].x=0.0
               		if punto[n].y<0.0005 and punto[n].y>-0.0005: punto[n].y=0.0
              		print "El punto ",n+1," es: ",punto[n].x,",",punto[n].y

class Inversa:
        def __init__(self,xp,yp):
                self.A=-2*l*(xp-(d/2))
                self.B=-2*yp*l
                self.C=(xp-(d/2))*(xp-(d/2)) + yp*yp + l*l - L*L
                self.e=-2*l*(xp+(d/2))
                self.f=(xp+(d/2))*(xp+(d/2)) + yp*yp + l*l - L*L
                
        def Q1(self):
                discriminanteq1=math.sqrt(self.B*self.B-(self.C*self.C-self.A*self.A))
                q1=math.degrees(2*math.atan((-self.B+sigmaq1*discriminanteq1)/(self.C-self.A)))
                return q1
        
        def Q2(self):
                discriminanteq2=math.sqrt(self.B*self.B-(self.f*self.f-self.e*self.e))
                q2=math.degrees(2*math.atan((-self.B+sigmaq2*discriminanteq2)/(self.f-self.e)))
                return q2

try:
	punto0=Punto()
	punto=[]
	Accion=False
	#listo1=False
	#listo2=False
	flanco1_pos=0
	flanco1_neg=0
	flanco2_pos=0
	flanco2_neg=0
	K1=1.0
	while(1):

		if Arduino1.inWaiting():
			Alpha1+=Leer_Alpha1()
			print "Alpha1:", Alpha1
		if Arduino2.inWaiting():
			Alpha2+=Leer_Alpha2()
			print "Alpha2:", Alpha2
		posActual=CinDirecta(Alpha1,Alpha2)
		print "posicion actual:", posActual
		
		if MODO=='LINEA_RECTA':
			Accion=True
			inversa=Inversa(punto[n].x,punto[n].y)
			q1=inversa.Q1()
			q2=inversa.Q2()
			if posActual[0]>=0.95*punto[n].x and posActual[0]<=1.05*punto[n].x and posActual[1]>=0.95*punto[n].y and posActual[1]<=1.05*punto[n].y:
			#if(listo1==True):# and listo2==True):
				if n<n_lados:
					n+=1
					#listo1=False
					#listo2=False
					print 'n:', n
				else:
					Accion=False
					#listo1=False
					#listo2=False
					MODO='NUEVO_POLIGONO'
					Arduino1.write('0000')
					Arduino2.write('0000')
		if MODO=='MODO_CENTRO':
			Accion=True
			inversa=Inversa(punto0.x,punto0.y)
			q1=inversa.Q1()
			q2=inversa.Q2()
			if posActual[0]>=0.95*punto0.x and posActual[0]<=1.05*punto0.x and posActual[1]>=0.95*punto0.y and posActual[1]<=1.05*punto0.y:
				Accion=False
				MODO='LINEA_RECTA'
				Arduino1.write('0000')
				Arduino2.write('0000')
				time.sleep(3)
		elif MODO=='NUEVO_POLIGONO':
			print ('POLIGONOOOS!!')
			Radio=input("Introduzca un radio: ")
			if Radio<=8:
				n_lados=input("Introduzca el numero de lados: ")
				alfarad=math.radians(360/n_lados) #angulo interno en radianes
				lado=2*Radio*math.sin(alfarad/2)
				#Declaracion de los puntos
				punto0.valor(X_centro,Y_centro)
				print "El punto central es: ",punto0.x,",",punto0.y
				Vertices()
				n=0
				MODO='MODO_CENTRO'
		elif MODO=='ARRANQUE':
			while Calibrado==False:
				if Calibrado1==False and Calibrado2==False:
					Arduino1.write('1250')
					Arduino2.write('1080')
				if GPIO.input(PIN_Fin1)==False:
					Arduino1.write('0000')
					Calibrado1=True
					print ("Calibrado Brazo 1")
				if GPIO.input(PIN_Fin2)==False:
					Arduino2.write('0000')
					Calibrado2=True
					print ("Calibrado Brazo 2")
				if Calibrado1 and Calibrado2:
					Calibrado=True
					MODO='NUEVO_POLIGONO'
		else:
			print ("ERROR")

		#Ley Control
		if Accion==True:
			error1=q1-Alpha1
			#print error1
			if(K1*error1)<-0.05:
			#	if flanco1_neg==0:
				print ('KK')
				Arduino1.write('1255')
				#	flanco1_neg=1
				#	flanco1_pos=0
			elif error1>0.05:
				#if flanco1_pos==0:
				print ('COCO')
				Arduino1.write('0255')
				#	flanco1_pos=1
				#	flanco1_neg=0
			else:
				Arduino1.write('0000')
				flanco1_pos=0
				flanco1_neg=0
				#listo1=True
				print("Saliendo")
			
			error2=q2-Alpha2
			if error2<-0.05:
		#		if flanco2_neg==0:
				print("KLK")
				Arduino2.write('1120')
				#	flanco2_neg=1
				#	flanco2_pos=0
			elif error2>0.05:
				print("K ASE")
				Arduino2.write('0120')
					#flanco2_pos=1
					#flanco2_neg=0
				
			else:
				Arduino2.write('0000')
				flanco2_pos=0
				flanco2_neg=0
				#listo2=True	
	
except KeyboardInterrupt:
	
	Arduino1.write('0000')
	Arduino2.write('0000')
	
			

