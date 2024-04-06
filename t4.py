from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests
from geopy.geocoders import Nominatim
import pyowm

#Initializing Database Connection
con = None 

root = Tk()
root.title("E-M-S")
root.iconbitmap("") #icon
root.geometry("500x600+50+50")
root.config(bg="lightblue")
f = ("Century", 15 , "bold")

#title
title_label = Label(root, text="Employee Management System", font=("Arial", 20, "bold"), bg="black", fg="lightblue")
title_label.pack(pady=10)


def add_employee():
	def save_employee():
		id_val = id_entry.get().strip()
		name_val = name_entry.get().strip()
		salary_val = salary_entry.get().strip()
        
		if id_val and name_val and salary_val:
			if not id_val.isdigit():
				messagebox.showerror("Error", "ID should be integer only")
	
			elif not name_val.isalpha():
				messagebox.showerror("Error", "NAME should only be alphabetic characters")
	
			elif not salary_val.replace(".", "", 1).isdigit() or float(salary_val) < 0:
				messagebox.showerror("Error", "SALARY must be a (+ve) positive value")
			else:
				try:
					con = connect("ems.db")
					cursor = con.cursor()
					sql = "insert into employee values(?, ?, ?)"
					cursor.execute(sql, (id_val , name_val, salary_val))
					con.commit()
					messagebox.showinfo("Success", "Employee added successfully!!!")
					add_window.destroy()
				except Exception as e:
					con.rollback()
					messagebox.showerror("Issue", "An error occured: " + str(e))
				finally:
					if con is not None:
						con.close()
		else:
			messagebox.showerror("Error", "Please fill in all fields")
	def go_back():
		add_window.destroy()
    
	add_window = Toplevel(root)
	add_window.title("Add Employee")
	add_window.geometry("300x400")

	id_label = Label(add_window, text="Enter Id:", font=f)
	id_label.pack(pady=5)
	id_entry = Entry(add_window, font=f)
	id_entry.pack(pady=5)
    
	name_label = Label(add_window, text="Enter Name:", font=f)
	name_label.pack(pady=5)
	name_entry = Entry(add_window, font=f)
	name_entry.pack(pady=5)
    
	salary_label = Label(add_window, text="Enter Salary:", font=f)
	salary_label.pack(pady=5)
	salary_entry = Entry(add_window, font=f)
	salary_entry.pack(pady=5)
    
	save_btn = Button(add_window, text="Save", font=f, command=save_employee)
	save_btn.pack(pady=10)

	back_btn = Button(add_window, text="Back", font=f, command=go_back)
	back_btn.pack(pady=10)


def view_employee():
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		print(data)

		view_window = Toplevel(root)
		view_window.title("View Employee")
		view_window.geometry("300x300")

		scrolled_view = ScrolledText(view_window, font=("Arial", 10, "bold"))
		scrolled_view.pack(expand=True)
		
		scrollbar = Scrollbar(view_window)
		scrollbar.pack(side=RIGHT, fill=Y)
		scrolled_view.configure(yscrollcommand=scrollbar.set)
		scrollbar.config(command=scrolled_view.yview)

		for d in data:
			text = "ID : " + str(d[0]) + ",  NAME : " + d[1] + ",  SALARY : " + str(d[2]) + "\n"
			scrolled_view.insert(END, text)

	except Exception as e:
		con.rollback()
		messagebox.showerror("Issue", "An error occured: " + str(e))
	finally:
		if con is not None:
			con.close()
	
	

def update_employee():
	def update_record():
		employee_id_str = employee_id_entry.get().strip()
		new_name = name_entry.get().strip()
		new_salary = salary_entry.get().strip()

		if employee_id_str.isdigit():
			employee_id = int(employee_id_str)
		
			if employee_id and new_name and new_salary:
				if not new_name.isalpha():
					messagebox.showerror("Error", "NAME should only be alphabetic characters")
	
				elif not new_salary.replace('.', '', 1).isdigit() or float(new_salary) < 0:
					messagebox.showerror("Error", "SALARY must be a (+ve) positive value")
				else:
					try:
						con = connect("ems.db")
						cursor = con.cursor()
#to check if employee id exists in database
						cursor.execute("SELECT * FROM employee WHERE id = ?", (employee_id,))
						if cursor.fetchone() is None:
							messagebox.showerror("Error", "Employee ID does not exist")
						else:
							sql = "update employee set name=?, salary=? where id=?"
							cursor.execute(sql, (new_name, new_salary, employee_id))
							con.commit()
							messagebox.showinfo("Success", "Employee updated successfully!!!")
							update_window.destroy()
				 
					except:
						con.rollback()
						messagebox.showerror("Issue", "An error occured: " + str(e))
						update_window.destroy()
					finally:
						if con is not None:
							con.close()		
			else:
				messagebox.showerror("Error", "Please fill in all fields")
		else:
			messagebox.showerror("Error", "ID should be integer only")


	def go_back():
		update_window.destroy()

	update_window = Toplevel(root)
	update_window.title("Update Employee")
	update_window.geometry("300x400")

	employee_id_label = Label(update_window, text = "Enter Id : ", font=f)
	employee_id_label.pack(pady=5)
	employee_id_entry = Entry(update_window, font=f)
	employee_id_entry.pack(pady=5)	

	name_label = Label(update_window, text = "Enter New Name : ", font=f)
	name_label.pack(pady=5)
	name_entry = Entry(update_window, font=f)
	name_entry.pack(pady=5)

	salary_label = Label(update_window, text = "Enter New Salary : ", font=f)
	salary_label.pack(pady=5)
	salary_entry = Entry(update_window, font=f)
	salary_entry.pack(pady=5)	

	save_btn = Button(update_window, text="Save", font=f, command=update_record)
	save_btn.pack(pady=10)

	back_btn = Button(update_window, text="Back", font=f, command=go_back)
	back_btn.pack(pady=10)



def delete_employee():
	def delete_record():
		employee_id = id_entry.get().strip()
		
		if employee_id:
			if not employee_id.isdigit():
				messagebox.showerror("Error", "ID should be integer only")
			else:	
				try:
					con = connect("ems.db")
					cursor = con.cursor()
					sql = "delete from employee where id = ?"
					cursor.execute(sql, (employee_id,))
					if cursor.rowcount == 1:
						con.commit()
						messagebox.showinfo("Success", "Employee deleted successfully!!!")
						delete_window.destroy()
					else:
						messagebox.showerror("Error", "Record Does not Exists :( ")
						delete_window.destroy()
				 
				except Exception as e:
					con.rollback()
					messagebox.showerror("Issue", "An error occured: " + str(e))
					delete_window.destroy()
				finally:
					if con is not None:
						con.close()
		else:
			messagebox.showerror("Error", "Please enter a valid employee ID!!!")
	def go_back():
		delete_window.destroy()

	delete_window = Toplevel(root)
	delete_window.title("Delete Employee")
	delete_window.geometry("300x300")

	id_label = Label(delete_window, text = "Employee ID : ", font=f)
	id_label.pack(pady=5)
	id_entry = Entry(delete_window, font=f)
	id_entry.pack(pady=5)
	
	delete_btn = Button(delete_window, text="Delete", font=f, command=delete_record)
	delete_btn.pack(pady=5)
		
	back_btn = Button(delete_window, text="Back", font=f, command=go_back)
	back_btn.pack(pady=5)


def charts_employee():
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from employee order by salary desc limit 5"
		cursor.execute(sql)
		data = cursor.fetchall()
		print(data)

		if data:
			names = [d[1] + "  (\u20B9" + str(d[2]) + ")" for d in data]
			salaries = [d[2] for d in data]

			plt.figure(figsize=(10, 6), num="Top 5 Chart")
			plt.bar(names, salaries, width=0.5)
			plt.xlabel('Name')
			plt.ylabel('Salary')
			plt.title("-*- Top 5 Highest-Earning Employees -*-")		
			plt.show()
		else:
			messagebox.showinfo("No Records", "No employee records found.")
	
	except Exception as e:
		con.rollback()
		messagebox.showerror("Issue", "An error occured: " + str(e))
	finally:
		if con is not None:
			con.close()


add_btn = Button(root, text="Add", font = f, command=add_employee)
add_btn.pack(pady=5)

view_btn = Button(root, text="View", font = f, command=view_employee)
view_btn.pack(pady=5)

update_btn = Button(root, text="Update", font = f,  command=update_employee)
update_btn.pack(pady=5)

delete_btn = Button(root, text="Delete", font = f, command=delete_employee)
delete_btn.pack(pady=5)

chart_btn = Button(root, text="Charts", font = f, command=charts_employee)
chart_btn.pack(pady=5)



def current_location():
	geolocator = Nominatim(user_agent="geoapiExercises")
	try:
		response = requests.get("https://ipinfo.io")
		data = response.json()
		city_country = data["city"]  + ", " + data["country"]
		location = geolocator.geocode(city_country)
		return location
	except Exception as e:
		return "Issue: " + str(e)


def current_temperature(location):
	try:
		owm = pyowm.OWM("571937787c7e3d8efbd694ec35e59e83")
		observation = owm.weather_manager().weather_at_coords(location.latitude, location.longitude)
		weather = observation.weather
		temperature = weather.temperature("celsius")["temp"]
		return temperature
	except Exception as e:
		return "Issue: " + str(e)

location_label = Label(root, text="", font=("Arial", 10, "bold"))
location_label.pack(pady=5)

temperature_label = Label(root, text="", font=("Arial", 10, "bold"))
temperature_label.pack(pady=5)


def update_weather_labels():
	location = current_location()
	if not isinstance(location, str):
		temperature = current_temperature(location)
		if not isinstance(temperature, str):
			location_label.config(text="Location: " + location.address)
			temperature_label.config(text="Temperature: " + str(temperature) + "°C")
		else:
			messagebox.showerror("Error", temperature)
	else:
		messagebox.showerror("Error", location)

update_weather_labels()




#exit msg box
def on_closing():
	if askyesno("Quit","Do you want to exit???"):
		try:
			if con is not None:
				con.close()
		except Exception as e:
			messagebox.showerror("Database Error(!)", "An error occurred while closing the database connection: " + str(e))
		
		root.destroy()
	
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()