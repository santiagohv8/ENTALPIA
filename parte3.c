#include <stdio.h>
#include <stdlib.h>

typedef struct estado{
unsigned int activo: 1;
unsigned int error: 1;
unsigned int bateria:7;
unsigned int operacion:4;
unsigned int signal:4;
}estado;
typedef struct sensor{
  int ID;
  float lectura;
  estado estadoSensor;
  struct sensor* siguiente;
}sensor;

sensor* crearSensor(int,float);
void insertarSensor(sensor**,int,float);
void eliminar(sensor**,int);
void mostrarLista(sensor*);
void liberarLista(sensor**);
void modEstado(sensor*,int,int,int,int,int,int);
void mostrarEstado(sensor*,int);

int main()
{
  sensor* lista = NULL;
  insertarSensor(&lista,10,12.65);
  insertarSensor(&lista,20,23.67);
  insertarSensor(&lista,30,89.09);

  mostrarLista(lista);

  modEstado(lista,20,1,0,97,2,4);
  mostrarEstado(lista,20);

  liberarLista(&lista);

  return 0;
}
void mostrarEstado(sensor* cabeza,int valor)
{
  sensor* temp = cabeza;
  while(temp!= NULL && temp->ID != valor)
  {
    temp = temp->siguiente;
  }
  if(temp == NULL)
  {
    return;
  }
  printf("Estado de sensor #%d: \n",temp->ID);
  printf("Actividad  Error Bateria Operacion Signal\n");
  printf("%s     %d     %d      %d         %d\n",temp->estadoSensor.activo == 1 ? "Activo":"Inactivo",temp->estadoSensor.error,temp->estadoSensor.bateria,temp->estadoSensor.operacion,temp->estadoSensor.signal);
}
void modEstado(sensor* cabeza,int valor,int activo,int error,int bateria,int ope, int sig)
{
  sensor* temp = cabeza;
  while(temp!= NULL && temp->ID != valor)
  {
    temp = temp->siguiente;
  }
  if(temp == NULL)
  {
    return;
  }

  temp->estadoSensor.activo = activo;
  temp->estadoSensor.error = error;
  temp->estadoSensor.bateria = bateria;
  temp->estadoSensor.operacion = ope;
  temp->estadoSensor.signal = sig;
}
void mostrarLista(sensor* cabeza)
{
  while(cabeza != NULL)
  {
    printf("[ID: %d | Lecturs: %.2f] -> ",cabeza->ID, cabeza->lectura);
    cabeza = cabeza->siguiente;
  }
  printf("NULL\n");
}
void liberarLista(sensor** cabeza)
{
  sensor* temp;
  while(*cabeza != NULL)
  {
    temp = *cabeza;
    *cabeza = (*cabeza)->siguiente;
    free(temp);
  }
}
void eliminar(sensor** cabeza, int valor)
{
  if(*cabeza == NULL)
  {
    return;
  }
  if((*cabeza)->ID == valor)
  {
    sensor* temp = *cabeza;
    *cabeza = (*cabeza)->siguiente;
    free(temp);
    return;
  }

  sensor* actual = *cabeza;
  while(actual->siguiente!= NULL && actual->siguiente->ID != valor)
  {
    actual = actual->siguiente;
  }
  if(actual->siguiente != NULL)
  {
    sensor* temp = actual->siguiente;
    actual->siguiente = temp->siguiente;
    free(temp);
  }


}
void insertarSensor(sensor** cabeza,int valor,float lectura)
{
  sensor* nuevo = crearSensor(valor,lectura);
  nuevo->siguiente = *cabeza;
  *cabeza = nuevo;
}
sensor* crearSensor(int valor, float lectura)
{
  sensor* nuevo = malloc(sizeof(sensor));
  nuevo->ID = valor;
  nuevo->lectura = lectura;
  nuevo->siguiente = NULL;
  return nuevo;
}