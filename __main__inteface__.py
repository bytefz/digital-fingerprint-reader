import serial, time
import serial_rx_tx
from tkinter import ttk
from tkinter import *

import sqlite3


class Programa():

	db_name = "base_de_datos.db"
 ## IG : 

	def __init__(self, ventana):
		self.vent = ventana
		self.vent.title("Edytec")

		#Framess
		frame = LabelFrame(self.vent, text = "User Register")
		frame.grid(row = 0, column= 0, columnspan = 3, pady = 20)
		
		#Nombres
		Label(frame, text = "Apellidos y Nombres:  ").grid(row = 1, column = 0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row = 1 , column = 1)

		#Entrada
		Label(frame, text = "DNI/RUC: ").grid(row = 2, column = 0)
		self.price = Entry(frame)
		self.price.grid(row = 2, column = 1)

		#Boton
		ttk.Button(frame, text = "Register", command = self.add_user).grid(row = 3, columnspan = 2, sticky = W + E)

		#mensajes
		self.message = Label(text = '', fg = "red")
		self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

		#Table
		self.tree = ttk.Treeview(height = 10, columns = 2)
		self.tree.grid(row = 4, column = 0, columnspan = 2)
		self.tree.heading("#0", text =  "Nombres y Apellidos", anchor = CENTER)
		self.tree.heading("#1", text = "DNI/RUC", anchor = CENTER)

		#Eliminar
		ttk.Button(text = "Borrar", command = self.delete_usuario).grid(row = 5, column = 0, sticky = W + E)
		ttk.Button(text = "Editar", command = self.edit_user).grid(row = 5, column = 1, sticky = W + E)

		self.get_products()

	def run_query(self, query, parameters = ()):
		with sqlite3.connect(self.db_name) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query, parameters)
			conn.commit()
		return result
	def get_products(self):

		#Limpiando
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)
		#Obteniendo Datos
		query = "SELECT * FROM Usuario ORDER BY Datos DESC"
		db_rows = self.run_query(query)
		for row in db_rows:
			self.tree.insert("", 0, text = row[0], values = row[1])


	def validation(self):
		return len(self.name.get()) != 0 and len(self.price.get()) != 0

	def add_user(self):
		if self.validation():
			query = "INSERT INTO Usuario VALUES(?, ?, NULL)"
			parameters = (self.name.get(), self.price.get())
			self.run_query(query, parameters)
			self.message["text"] = "Usuario {} ha sido añadido".format(self.name.get())
			self.name.delete(0,END)
			self.price.delete(0,END)
		else:
			self.message["text"] = "El Usuario o DNI es requerido"

		self.get_products()
	def delete_usuario(self):
		self.message["text"] = ""
		try:
			self.tree.item(self.tree.selection())["text"][0]
		except IndexError as e:
			self.message["text"] = "Seleccione un Usuario"
			return
		self.message["text"] = ""
		name = self.tree.item(self.tree.selection())["text"]
		query = "DELETE FROM Usuario WHERE Datos = ?"
		self.run_query(query,(name, ))
		self.message["text"] = "Usuario {} ha sido eliminado satisfactoriamente".format(name)
		self.get_products()

	def edit_user(self):
		self.message["text"] = ""
		try:
			self.tree.item(self.tree.selection())["text"][0]
		except IndexError as e:
			self.message["text"] = "Seleccione un Usuario"
			return
		name = self.tree.item(self.tree.selection())["text"]
		old_price = self.tree.item(self.tree.selection())["values"][0]
		self.edit_vent = Toplevel()
		self.edit_vent.title = "Edit User"

		#Usuario Antiguo
		Label(self.edit_vent, text = "Old Usuario: ").grid(row = 0, column = 1)
		Entry(self.edit_vent, textvariable = StringVar(self.edit_vent, value = name), state = "readonly").grid(row = 0, column = 2)
		#Nuevo usuario
		Label(self.edit_vent, text = "New User").grid(row = 1, column = 1)
		new_user = Entry(self.edit_vent)
		new_user.grid(row = 1, column =2)

		#Old DNI/RUC
		Label(self.edit_vent, text = "Old DNI/RUC").grid(row = 2, column = 1)
		Entry(self.edit_vent, textvariable = StringVar(self.edit_vent, value = old_price), state = "readonly").grid(row = 2, column = 2)
		#New DNI/RUC
		Label (self.edit_vent, text = "New DNI/RUC").grid(row = 3, column = 1)
		new_price = Entry(self.edit_vent)
		new_price.grid(row =3, column =2)

		Button(self.edit_vent, text = "Actualizar",command = lambda: self.edit_records(new_user.get(), name, new_price.get(),old_price)).grid( row = 4, column = 2, sticky = W )

	
	def edit_records(self,new_user, name, new_price, old_price):
		query = "UPDATE Usuario SET Datos = ?, RUC = ? WHERE Datos = ? AND RUC = ?"	
		parameters = (new_user, new_price, name, old_price)
		self.run_query(query,parameters)
		self.edit_vent.destroy()
		self.message["text"] = "El Usuario {} ha sido Actualizado".format(name)
		self.get_products()

if __name__ == "__main__":
	ventana = Tk()
	aplicacion = Programa(ventana)
	ventana.mainloop()