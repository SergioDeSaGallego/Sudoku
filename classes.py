import tkinter as tk
import random
import copy

class Celda_f(tk.Frame):
    def __init__(self, master, f_col, f_row):
        super().__init__(master)

        
        borde_superior = 2 if f_row % 3 == 0 else 1
        borde_inferior = 2 if f_row % 3 == 2 else 1
        borde_izquierdo = 2 if f_col % 3 == 0 else 1
        borde_derecho = 2 if f_col % 3 == 2 else 1
        
        
        self.config(bg="black", highlightbackground="black", highlightthickness=0, bd=0)
        self.grid(row=f_row, column=f_col)
        
        self.celda=tk.Entry(self, width=2, font=("Arial",17), bg="white", justify="center")
        self.celda.grid(ipadx=22, ipady=22, padx=(borde_izquierdo, borde_derecho), pady=(borde_superior,borde_inferior))
        
        
class Celda_g(tk.Frame):
    def __init__(self, master, f_col, f_row, numero):
        super().__init__(master)
        
        borde_superior = 2 if f_row % 3 == 0 else 1
        borde_inferior = 2 if f_row % 3 == 2 else 1
        borde_izquierdo = 2 if f_col % 3 == 0 else 1
        borde_derecho = 2 if f_col % 3 == 2 else 1

        self.config(bg="black", highlightbackground="black", highlightthickness=0, bd=1)
        self.grid(row=f_row, column=f_col)

        self.celda = tk.Label(self, text=numero, width=2, font=("Arial", 17), bg="lightgray")
        self.celda.grid(ipadx=22, ipady=22, padx=(borde_izquierdo, borde_derecho), pady=(borde_superior, borde_inferior))

        
class Generar_sudoku():
    def __init__(self):
        self.sudoku_guardado={}
        self.todas_las_celdas=[]
        self.diccionario_vacias={}
        self.generar_numeros()
        
    def comprobar_numero(self,x,y,numero):
        for i in range(9):
            if (i,y) in self.sudoku_guardado and self.sudoku_guardado[(i,y)]==numero:
                return False
            
        for i in range(9):
            if (x,i) in self.sudoku_guardado and self.sudoku_guardado[(x,i)]==numero:
                return False
        
        start_x=(x//3)*3
        start_y=(y//3)*3
        for j in range(3):
            for k in range(3):
                if (start_x+j,start_y+k) in self.sudoku_guardado and self.sudoku_guardado[(start_x+j,start_y+k)]==numero:
                    return False
        return True

    def generar_numeros(self,x=0,y=0):
        if y==9:
            return True
        
        if x<8:
            siguiente_y=y
            siguiente_x=x+1
        else:
            siguiente_y=y+1
            siguiente_x=0
        

        lista_random=list(range(1,10))
        random.shuffle(lista_random)
        
        for i in lista_random:
            if self.comprobar_numero(x,y,i):
                self.sudoku_guardado[(x,y)]=i
                if self.generar_numeros(siguiente_x,siguiente_y):
                    return True
                del self.sudoku_guardado[(x,y)]
        return False

    def nuevo_sudoku(self, caja, max_empty_cells, empty_cells=0):
        self.sudoku_guardado.clear()
        self.diccionario_vacias.clear()
        for i in self.todas_las_celdas:
            i.destroy()
        self.todas_las_celdas.clear()
        self.generar_numeros()
        
        sudoku_preparado=copy.deepcopy(self.sudoku_guardado)
        

        while empty_cells<max_empty_cells:
            x=random.randint(0,8)
            y=random.randint(0,8)
            if sudoku_preparado[(x,y)]!=".":
                sudoku_preparado[(x,y)]="."
                sudoku_a_comprobar=copy.deepcopy(sudoku_preparado)
                
                if self.filtro(sudoku_a_comprobar) == 1:
                    empty_cells+=1
                else:
                    sudoku_preparado[(x,y)]=self.sudoku_guardado[(x,y)]
                    
        for i in sudoku_preparado:
            if sudoku_preparado[(i[0],i[1])]==".":
                cell=Celda_f(caja,i[0],i[1])
                self.diccionario_vacias[i]=cell
            else:
                cell=Celda_g(caja,i[0],i[1],sudoku_preparado[(i[0],i[1])])
                
            self.todas_las_celdas.append(cell)
            
                
        print(f"{empty_cells} celdas vacías.")            
        

            
    def comprobar_numero_del_filtro(self,x,y,numero,sudoku_preparado):
        for i in range(9):
            if (i,y) in sudoku_preparado and sudoku_preparado[(i,y)]==numero:
                return False
            
        for i in range(9):
            if (x,i) in sudoku_preparado and sudoku_preparado[(x,i)]==numero:
                return False
        
        start_x=(x//3)*3
        start_y=(y//3)*3
        for j in range(3):
            for k in range(3):
                if (start_x+j,start_y+k) in sudoku_preparado and sudoku_preparado[(start_x+j,start_y+k)]==numero:
                    return False
        return True
        
    def filtro(self, sudoku_inspeccionado, soluciones = 0):
        
        if soluciones > 1:  
            return soluciones

        for i in sudoku_inspeccionado:
            if sudoku_inspeccionado[i] == ".":
                for numero in range(1, 10):
                    if self.comprobar_numero_del_filtro(i[0], i[1], numero, sudoku_inspeccionado):
                        sudoku_inspeccionado[i] = numero
                        soluciones = self.filtro(sudoku_inspeccionado, soluciones)
                        if soluciones > 1:  
                            return soluciones
                        sudoku_inspeccionado[i] = "."
                        
                return soluciones

        return soluciones + 1
