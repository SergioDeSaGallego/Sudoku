from classes import Generar_sudoku
import tkinter as tk
import random



sudoku = Generar_sudoku()

caja=tk.Tk()
caja.title("Sudoku")

numero=tk.IntVar(value=0)
pistas_restantes=tk.IntVar(value=3)
puntos_fase=tk.IntVar(value=0)
puntos_totales=tk.IntVar(value=0)
fase_completada=tk.IntVar(value=0)
fase_inicial=tk.IntVar(value=1)


        
def nueva_escena(dificultad):
    numero.set(numero.get()+1)
    print("\033c\033[3J", end='')
    if fase_completada.get() == 0 and fase_inicial.get() == 0:
        print(f"Fase no completada, se perderán {puntos_fase.get()} puntos")
        puntos_totales.set(puntos_totales.get()-puntos_fase.get())
        puntuacion_total.config(text=f"Puntuación total {puntos_totales.get()}")
    
    fase_completada.set(0)
    fase_inicial.set(0)
    
    if dificultad == "facil":
        sudoku.nuevo_sudoku(caja,33,False)
        caja.title(f"Sudoku nº {numero.get()}. Dificultad fácil")
        puntos_fase.set(0)
        pistas_restantes.set(3)
        boton_p["state"]="normal"
        boton_p["text"]=f"Pedir pista\n{pistas_restantes.get()}"
    elif dificultad == "normal":
        sudoku.nuevo_sudoku(caja,42,False)
        caja.title(f"Sudoku nº {numero.get()}. Dificultad normal")
        puntos_fase.set(50)
        pistas_restantes.set(3)
        boton_p["state"]="normal"
        boton_p["text"]=f"Pedir pista\n{pistas_restantes.get()}" 
    elif dificultad == "dificil":
        sudoku.nuevo_sudoku(caja,52,False)
        caja.title(f"Sudoku nº {numero.get()}. Dificultad difícil")
        puntos_fase.set(70)
        pistas_restantes.set(3)
        boton_p["state"]="normal"
        boton_p["text"]=f"Pedir pista\n{pistas_restantes.get()}"

    puntuacion_total.grid()
    boton_p.grid()
    boton_pl.grid()
    boton_r.grid()
    boton_r["state"]="normal"
    puntuacion_fase.config(text=f"Puntuación por fase {puntos_fase.get()}")
    puntuacion_fase.grid()


def pista():
    celdas_a_resolver=sudoku.diccionario_vacias
    celdas_en_blanco=[]
    celdas_incorrectas=[]
    puntos_fase.set(puntos_fase.get()-10)
    puntuacion_fase.config(text=f"Puntuación por fase {puntos_fase.get()}")
    pistas_restantes.set(pistas_restantes.get()-1)
    
    if pistas_restantes.get() == 0 : boton_p["state"]="disabled"
    if pistas_restantes.get()>=0:
        print(f"Gastada una pista, -10 a los puntos ganados.")
        boton_p["text"]=f"Pedir pista\n{pistas_restantes.get()}\n(-10 puntos)"
        for i in celdas_a_resolver:
            if celdas_a_resolver[i].celda.get() == "":
                celdas_en_blanco.append(i)
            elif (celdas_a_resolver[i].celda.get().isnumeric())==False or int(celdas_a_resolver[i].celda.get()) != int(sudoku.sudoku_guardado[i]):
                celdas_incorrectas.append(i)


        def pista_nueva(celda):
            celdas_a_resolver[celda].celda.delete(0,9999999)
            celdas_a_resolver[celda].celda.insert(0,sudoku.sudoku_guardado[celda])
            celdas_a_resolver[celda].celda.config(bg="red")

        if celdas_incorrectas and celdas_en_blanco:
            pista_prob=random.randint(0,9)
            if pista_prob>3:
                pista_nueva(random.choice(celdas_incorrectas))
            else:
                pista_nueva(random.choice(celdas_en_blanco))
        elif celdas_incorrectas:
            pista_nueva(random.choice(celdas_incorrectas))
        elif celdas_en_blanco:
            pista_nueva(random.choice(celdas_en_blanco))


def limpiar_pistas():
    dic_celdas_respuestas=sudoku.diccionario_vacias
    for i in dic_celdas_respuestas:
        dic_celdas_respuestas[i].celda.config(bg="white")

            
def resolver():
    dic_celdas_respuestas=sudoku.diccionario_vacias
    fallos=0
    boton_r["state"]="disabled"
    for i in dic_celdas_respuestas:
        if dic_celdas_respuestas[i].celda.get() != "":
            if (dic_celdas_respuestas[i].celda.get().isnumeric()) and int(dic_celdas_respuestas[i].celda.get()) == int(sudoku.sudoku_guardado[i]):
                dic_celdas_respuestas[i].celda.config(bg="lightgreen", highlightbackground="black")
            else:
                dic_celdas_respuestas[i].celda.config(bg="red", highlightbackground="black")
                fallos+=1
                print(f"En la fila {i[1]+1}, columna {i[0]+1} tienes '{dic_celdas_respuestas[i].celda.get()}', debería ser '{sudoku.sudoku_guardado[i]}'")
                dic_celdas_respuestas[i].celda.delete(0,9999999)
                dic_celdas_respuestas[i].celda.insert(0,int(sudoku.sudoku_guardado[i]))
                
        else:
            dic_celdas_respuestas[i].celda.config(bg="orange", highlightbackground="black")
            fallos+=1
            print(f"la fila {i[1]+1}, columna {i[0]+1} está vacía!")
            dic_celdas_respuestas[i].celda.delete(0)
            dic_celdas_respuestas[i].celda.insert(0,int(sudoku.sudoku_guardado[i]))
            
    if fallos==0:
        print(f"Fase completada! :D ganas {puntos_fase.get()} puntos.")
        puntos_totales.set(puntos_totales.get()+puntos_fase.get())
        puntuacion_total.config(text=f"Puntuación total {puntos_totales.get()}")
    else:
        print(f"Fase fallida! :( Pierdes {puntos_fase.get()} puntos.")
        puntos_totales.set(puntos_totales.get()-puntos_fase.get())
        puntuacion_total.config(text=f"Puntuación total {puntos_totales.get()}")
    fase_completada.set(1)


puntuacion_total=tk.Label(caja, text=f"Puntuación total {puntos_totales.get()}", height=2, font=("Arial"))
puntuacion_total.grid(row=0,column=9, sticky="wn")
puntuacion_total.grid_remove()

puntuacion_fase=tk.Label(caja, height=2, font=("Arial"))
puntuacion_fase.grid(row=0,column=9, sticky="ws")
puntuacion_fase.grid_remove()

boton_f=tk.Button(caja, text="Fácil", pady=6, command=lambda:nueva_escena("facil"))
boton_f.grid(row=1,column=9, sticky="news")
boton_m=tk.Button(caja, text="Normal", pady=6, command=lambda:nueva_escena("normal"))
boton_m.grid(row=2,column=9, sticky="eswn")
boton_d=tk.Button(caja, text="Difícil", pady=6, command=lambda:nueva_escena("dificil"))
boton_d.grid(row=3,column=9, sticky="news")

boton_p=tk.Button(caja, text=f"Pedir pista {pistas_restantes.get()}", pady=0, command=lambda:pista(), bg="gold")
boton_p.grid(row=7,column=9,sticky="snew")
boton_p.grid_remove()

boton_pl=tk.Button(caja, text="Limpiar pistas", pady=6, command=(lambda:limpiar_pistas()), fg="white", bg="darkgrey")
boton_pl.grid(row=8,column=9,sticky="new")
boton_pl.grid_remove()

boton_r=tk.Button(caja, text="Resolver", pady=6, command=lambda:resolver(), bg="green")
boton_r.grid(row=8,column=9, sticky="ews")
boton_r.grid_remove()



caja.mainloop()