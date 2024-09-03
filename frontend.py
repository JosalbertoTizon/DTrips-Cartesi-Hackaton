import customtkinter as ctk
import backend
import tkintermapview

class App:
    def __init__(self):
        self.main_window = ctk.CTk()
        self.main_window_title = ctk.CTkLabel(self.main_window, text="Welcome to Dtrips", font=("Helvetica", 30, "bold"))
        self.main_window_signin_frame = ctk.CTkFrame(self.main_window, width=360, height=300)
        self.main_window_signup_frame = ctk.CTkFrame(self.main_window, width=360, height=100)
        self.main_window_usertype_text = ctk.CTkLabel(self.main_window_signin_frame, text="Choose user type", font=("Helvetica", 15, "bold"))
        self.main_window_usertype_button = ctk.CTkSegmentedButton(self.main_window_signin_frame, values=["      Driver      ", "      Rider      "], selected_color="DodgerBlue3", selected_hover_color="SteelBlue", width=150, height=24, font=("Helvetica", 12, "bold"), corner_radius=12)
        self.main_window_signin_text = ctk.CTkLabel(self.main_window_signin_frame, text="Sign in to your account", font=("Helvetica", 15, "bold"))
        self.main_window_name = ctk.CTkEntry(self.main_window_signin_frame, width=280, height=24, placeholder_text="username", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.main_window_password = ctk.CTkEntry(self.main_window_signin_frame, width=280, height=24, placeholder_text="password", show="•", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.main_window_signin_button = ctk.CTkButton(self.main_window_signin_frame, width = 150, height=24, text="Sign in", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_signin, corner_radius=12, state="disabled", text_color_disabled="LightBlue4")
        self.main_window_feedback = ctk.CTkLabel(self.main_window_signin_frame, text="", font=("Helvetica", 15, "bold"))
        self.main_window_signup_text = ctk.CTkLabel(self.main_window_signup_frame, text="Don't have an account?", font=("Helvetica", 15, "bold"))
        self.main_window_signup_button = ctk.CTkButton(self.main_window_signup_frame, width=150, height=24, text="Sign up", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_signup, corner_radius=12)
        self.main_window_closeapp_button = ctk.CTkButton(self.main_window, width=100, height=24, text="Close app", fg_color="firebrick3", hover_color="indianred3", font=("Helvetica", 12, "bold"), command=self.__handle_closeapp, corner_radius=12)
    
    def build_app(self):
        self.main_window.attributes("-fullscreen", True)
        self.main_window.title("Ddrive")
        self.main_window_title.place(relx=0.5, rely=0.15, anchor="center")
        self.main_window_signin_frame.place(relx=0.5, rely=0.4, anchor="center")
        self.main_window_signup_frame.place(relx=0.5, rely=0.61, anchor="center")
        self.main_window_usertype_text.place(relx=0.5, rely=0.14, anchor="center")
        self.main_window_usertype_button.place(relx=0.5, rely=0.26, anchor="center")
        self.main_window_usertype_button.set("      Rider      ")
        self.main_window_signin_text.place(relx=0.5, rely=0.38, anchor="center")
        self.main_window_name.place(relx=0.5, rely=0.50, anchor="center")
        self.main_window_password.place(relx=0.5, rely=0.62, anchor="center")
        self.main_window_signin_button.place(relx=0.5, rely=0.74, anchor="center")
        self.main_window_feedback.place(relx=0.5, rely=0.86, anchor="center")
        self.main_window_signup_text.place(relx=0.5, rely=0.3, anchor="center")
        self.main_window_signup_button.place(relx=0.5, rely=0.7, anchor="center")
        self.main_window_name.bind(sequence="<KeyRelease>", command=self.__update_signin_button)
        self.main_window_password.bind(sequence="<KeyRelease>", command=self.__update_signin_button)
        self.main_window_closeapp_button.place(relx=0.95, rely=0.05, anchor="center")
    def run_app(self):
        self.main_window.mainloop()
    
    def __update_signin_button(self, event=None):
        user_name = self.main_window_name.get()
        user_password = self.main_window_password.get()
        if user_name and user_password:
            self.main_window_signin_button.configure(state="normal")
        else:
            self.main_window_signin_button.configure(state="disabled")
    def __handle_signin(self):
        self.user_data={"usertype": None, "name": None, "password": None}
        if str(self.main_window_usertype_button.get()) == "      Driver      ":
            self.user_data["usertype"] = "Driver"
        if str(self.main_window_usertype_button.get()) == "      Rider      ":
            self.user_data["usertype"] = "Rider"
        self.user_data["name"] = str(self.main_window_name.get())
        self.user_data["password"] = str(self.main_window_password.get())
        backend_feedback = backend.login(self.user_data["name"], self.user_data["password"])
        if backend_feedback[0] == "connect":
            self.main_window_feedback.configure(text="Connection problem, try again later", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback[0] == "register":
            self.main_window_feedback.configure(text="User not registered", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback[0] == "success":
            if self.user_data["usertype"] == backend_feedback[1] and self.user_data["usertype"] == "Driver":
                self.main_window_title.place_forget()
                self.main_window_signin_frame.place_forget()
                self.main_window_signup_frame.place_forget()
                self.signin = DriverSignin(self, self.main_window, self.user_data["name"])
                self.signin.build_signin()
            if self.user_data["usertype"] == backend_feedback[1] and self.user_data["usertype"] == "Rider":
                self.main_window_title.place_forget()
                self.main_window_signin_frame.place_forget()
                self.main_window_signup_frame.place_forget()
                self.signin = RiderSignin(self, self.main_window, self.user_data["name"])
                self.signin.build_signin()
            if self.user_data["usertype"] != backend_feedback[1]:
                self.main_window_feedback.configure(text="User type do not match", font=("Helvetica", 15, "bold"), text_color="red")
        
    def __handle_signup(self):
        self.main_window_title.place_forget()
        self.main_window_signin_frame.place_forget()
        self.main_window_signup_frame.place_forget()
        self.signup = Signup(self, self.main_window)
        self.signup.build_signup()
    
    def __handle_closeapp(self):
        self.main_window.destroy()
        
class Signup:
    def __init__(self, app, root):
        self.app = app
        self.signup_window_title = ctk.CTkLabel(root, text="Create account", font=("Helvetica", 30, "bold"))
        self.signup_window_frame = ctk.CTkFrame(root, width=360, height=300)
        self.signup_window_text = ctk.CTkLabel(self.signup_window_frame, text="Insert name, user type, email and password", font=("Helvetica", 15, "bold"))
        self.signup_window_name = ctk.CTkEntry(self.signup_window_frame, width=280, height=24, placeholder_text="username", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_email = ctk.CTkEntry(self.signup_window_frame, width=280, height=24, placeholder_text="email", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_password = ctk.CTkEntry(self.signup_window_frame, width=280, height=24, placeholder_text="password", show="•", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_confirmpassword = ctk.CTkEntry(self.signup_window_frame, width=280, height=24, placeholder_text="confirm password", show="•", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_wallet_account = ctk.CTkEntry(self.signup_window_frame, width=280, height=24, placeholder_text="accound id", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_usertype_button = ctk.CTkSegmentedButton(self.signup_window_frame, values=["      Driver      ", "      Rider      "], selected_color="DodgerBlue3", selected_hover_color="SteelBlue", width=150, height=24, font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signup_window_button = ctk.CTkButton(self.signup_window_frame, width=150, height=24, text="Sign up", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__new_signup, corner_radius=12, state="disabled", text_color_disabled="LightBlue4")
    
    def build_signup(self):
        self.signup_window_title.place(relx=0.5, rely=0.15, anchor="center")
        self.signup_window_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.signup_window_text.place(relx=0.5, rely=0.11, anchor="center")
        self.signup_window_usertype_button.place(relx=0.5, rely=0.22, anchor="center")
        self.signup_window_usertype_button.set("      Rider      ")
        self.signup_window_name.place(relx=0.5, rely=0.33, anchor="center")
        self.signup_window_email.place(relx=0.5, rely=0.44, anchor="center")
        self.signup_window_password.place(relx=0.5, rely=0.55, anchor="center")
        self.signup_window_confirmpassword.place(relx=0.5, rely=0.66, anchor="center")
        self.signup_window_wallet_account.place(relx=0.5, rely=0.77, anchor="center")
        self.signup_window_button.place(relx=0.5, rely=0.88, anchor="center")
        self.signup_window_name.bind(sequence="<KeyRelease>", command=self.__update_signup_button)
        self.signup_window_email.bind(sequence="<KeyRelease>", command=self.__update_signup_button)
        self.signup_window_password.bind(sequence="<KeyRelease>", command=self.__update_signup_button)
        self.signup_window_confirmpassword.bind(sequence="<KeyRelease>", command=self.__update_signup_button)
        self.signup_window_wallet_account.bind(sequence="<KeyRelease>", command=self.__update_signup_button)
    
    def __update_signup_button(self, event=None):
        user_name = self.signup_window_name.get()
        user_email = self.signup_window_email.get()
        user_password = self.signup_window_password.get()
        user_confirmpassword = self.signup_window_confirmpassword.get()
        user_wallet_account = self.signup_window_wallet_account.get()
        if user_name and user_email and user_password and user_confirmpassword and user_wallet_account:
            self.signup_window_button.configure(state="normal")
        else:
            self.signup_window_button.configure(state="disabled")            
    
    def __new_signup(self):
        self.user_data = {"usertype":None, "name":None, "email":None, "password":None, "confirmpassword":None, "wallet":None}
        if str(self.signup_window_usertype_button.get()) == "      Rider      ":
            self.user_data["usertype"] = "Rider"
        if str(self.signup_window_usertype_button.get()) == "      Driver      ":
            self.user_data["usertype"] = "Driver"
        self.user_data["name"] = str(self.signup_window_name.get())
        self.user_data["email"] = str(self.signup_window_email.get())
        self.user_data["password"] = str(self.signup_window_password.get())
        self.user_data["confirmpassword"] = str(self.signup_window_confirmpassword.get())
        self.user_data["wallet"] = str(self.signup_window_wallet_account.get())
        if self.user_data["confirmpassword"] != self.user_data["password"]:
            self.signup_window_title.place_forget()
            self.signup_window_frame.place_forget()
            self.app.build_app()
            self.app.main_window_feedback.configure(text="Password was not confirmed due to difference", font=("Helvetica", 15, "bold"), text_color="red")
        else:
            backend_feedback = backend.sign_up(self.user_data["usertype"], self.user_data["name"], self.user_data["password"], self.user_data["wallet"], self.user_data["email"])
            self.signup_window_title.place_forget()
            self.signup_window_frame.place_forget()
            self.app.build_app()
            if backend_feedback == "connect":
                self.app.main_window_feedback.configure(text="Connection problem, try again later", font=("Helvetica", 15, "bold"), text_color="red")
            if backend_feedback == "register":
                self.app.main_window_feedback.configure(text="Username already exists", font=("Helvetica", 15, "bold"), text_color="red")
            if self.user_data["confirmpassword"] == self.user_data["password"] and backend_feedback == "success":
                self.app.main_window_feedback.configure(text="Account created succesfuly", font=("Helvetica", 15, "bold"), text_color="green")
        
        
class DriverSignin:
    def __init__(self, app, root, name):
        self.app = app
        self.name = name
        self.address = None
        self.currentbalance = None
        self.signin_stats_frame = ctk.CTkFrame(root, width=400, height=900)
        self.signin_stats_frame_title = ctk.CTkLabel(self.signin_stats_frame, text=f"Welcome {self.name}", font=("Helvetica", 30, "bold"))
        self.signin_riders_frame = ctk.CTkFrame(self.signin_stats_frame, width=300, height=270)
        self.signin_riders_frame_text = ctk.CTkLabel(self.signin_riders_frame, text="Search for a rider", font=("Helvetica", 15, "bold"))
        self.signin_riders_address = ctk.CTkEntry(self.signin_riders_frame, width=250, height=24, placeholder_text="insert current address", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signin_riders_validate_button = ctk.CTkButton(self.signin_riders_frame, width=150, height=24, text="Validate address", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_validation, corner_radius=12, state="disabled")
        self.signin_riders_search_button = ctk.CTkButton(self.signin_riders_frame, width=150, height=24, text="Search nearby riders", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), corner_radius=12, command=self.__handle_location, state="disabled")
        self.signin_riders_accept_button = ctk.CTkButton(self.signin_riders_frame, width=150, height=24, text="Accept rider", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), corner_radius=12, command=self.__handle_ride, state="disabled")
        self.signin_riders_feedback = ctk.CTkLabel(self.signin_riders_frame, text="", font=("Helvetica", 15, "bold"))
        self.signin_riders_list = ctk.CTkOptionMenu(self.signin_riders_frame, width=250, height=24, button_color="DodgerBlue3", button_hover_color="SteelBlue", font=("Helvetica", 12, "bold"), corner_radius=12, values=[], state="disabled", text_color_disabled="DodgerBlue3")
        self.signin_map_frame = ctk.CTkFrame(root, width=1350, height=900)
        self.signin_wallet_frame = ctk.CTkFrame(self.signin_stats_frame, width=300, height=400)
        self.signin_wallet_balance = ctk.CTkLabel(self.signin_wallet_frame, text="Your balance:", font=("Helvetica", 20, "bold"))
        self.signin_wallet_money = ctk.CTkLabel(self.signin_wallet_frame, text="", font=("Helvetica", 15, "bold"))
        self.signin_wallet_money_button = ctk.CTkButton(self.signin_wallet_frame, width=150, height=24, text="Show balance", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), corner_radius=12, command=self.__handle_balance)
        self.signin_wallet_frame_title = ctk.CTkLabel(self.signin_wallet_frame, text="Wallet", font=("Helvetica", 30, "bold"))
        self.signout_button = ctk.CTkButton(self.signin_stats_frame, width=150, height=24, text="Sign out", fg_color="firebrick3", hover_color="indianred3", font=("Helvetica", 12, "bold"), command=self.__new_signin, corner_radius=12)
    
    def build_signin(self):
        self.signin_stats_frame.place(relx=0.135, rely=0.5, anchor="center")
        self.signin_stats_frame_title.place(relx=0.5, rely=0.1, anchor="center")
        self.signin_riders_frame.place(relx=0.5, rely=0.3, anchor="center")
        self.signin_riders_frame_text.place(relx=0.5, rely=0.14, anchor="center")
        self.signin_riders_address.place(relx=0.5, rely=0.26, anchor="center")
        self.signin_riders_list.place(relx=0.5, rely=0.38, anchor="center")
        self.signin_riders_validate_button.place(relx=0.5, rely=0.50, anchor="center")
        self.signin_riders_search_button.place(relx=0.5, rely=0.62, anchor="center")
        self.signin_riders_accept_button.place(relx=0.5, rely=0.74, anchor="center")
        self.signin_riders_feedback.place(relx=0.5, rely=0.86, anchor="center")
        self.signin_map_frame.place(relx=0.619, rely=0.5, anchor="center")
        self.signin_wallet_frame.place(relx=0.5, rely=0.70, anchor="center")
        self.signin_wallet_frame_title.place(relx=0.5, rely=0.1, anchor="center")
        self.signin_wallet_balance.place(relx=0.5, rely=0.3, anchor="center")
        self.signin_wallet_money.place(relx=0.5, rely=0.5, anchor="center")
        self.signin_wallet_money_button.place(relx=0.5, rely=0.7, anchor="center")
        self.signout_button.place(relx=0.5, rely=0.96, anchor="center")
        self.signin_riders_address.bind(sequence="<KeyRelease>", command=self.__update_riders_validate_button)

    def __update_riders_validate_button(self, event=None):
        user_address = self.signin_riders_address.get()
        if user_address:
            self.signin_riders_validate_button.configure(state="normal")
    
    def __handle_balance(self):
        account = backend.get_account(self.name)
        self.currentbalance = backend.fetch()[str(account)]
        self.signin_wallet_money.configure(text=f"Ridecoin: {self.currentbalance}")
    
    def __handle_validation(self):
        valid = backend.validation_address(self.signin_riders_address.get())
        if valid == "Valid address":
            self.signin_riders_search_button.configure(state="normal")
            self.signin_riders_feedback.configure(text="Address validation successful", text_color="green")
        if valid == "Invalid address":
            self.signin_riders_feedback.configure(text="The provided address is not valid", text_color="red")

    def __handle_location(self):
        user_address = str(self.signin_riders_address.get())
        self.address = user_address
        backend_feedback = backend.driver_location(self.name, user_address)
        if backend_feedback == "error":
            self.signin_riders_feedback.configure(text="There was an error, try again later", text_color="red")
        if backend_feedback == "success":
            rides, backend_feedback2 = backend.rides_for_driver(self.name)
            if backend_feedback2 == "error":
                self.signin_riders_feedback.configure(text="There was an error, try again later", text_color="red")
            if backend_feedback2 == "success":
                self.signin_riders_list.configure(state="normal")
                self.signin_riders_feedback.configure(text="Rides found", text_color="green")
                show_rides=[]
                for ride in rides:
                    show_ride_name = ride["name"]
                    show_ride_start = ride["start_address"]
                    show_ride_end = ride["end_address"]
                    show_ride_distance = "{:.2}".format(ride["distance"])
                    show_ride_duration = "{:.2}".format(ride["duration"])
                    show_ride = f"{show_ride_name} | {show_ride_start} | {show_ride_end} | {show_ride_distance} km | {show_ride_duration} min"
                    show_rides.append(show_ride)
                self.signin_riders_list.configure(values=show_rides)
                self.signin_riders_accept_button.configure(state="normal")
    
    def __handle_ride(self):
        selected_ride = self.signin_riders_list.get().split(" | ")
        backend_feedback = backend.rides_in_progress(selected_ride[0], self.name, selected_ride[1], selected_ride[2])
        if backend_feedback == "error":
            self.signin_riders_feedback.configure(text="There was an error, try again later", text_color="red")
        if backend_feedback == "success":
            self.signin_riders_feedback.configure(text="Ride confirmed, go to the rider's location", text_color="green")
            
            driver_lat, driver_lng = backend.get_coordinates(self.address)
            start_lat, start_lng = backend.get_coordinates(selected_ride[1])
            end_lat, end_lng = backend.get_coordinates(selected_ride[2])
            _, _, route_coords = backend.get_distance_and_duration(selected_ride[1], selected_ride[2], backend.api_key)
            
            # Converte as coordenadas para float
            start_lat = float(start_lat)
            start_lng = float(start_lng)
            end_lat = float(end_lat)
            end_lng = float(end_lng)
            driver_lat = float(driver_lat)
            driver_lng = float(driver_lng)
            
            root = self.signin_map_frame.winfo_toplevel()
            root.title('mapa')
            try:
                map_widget = tkintermapview.TkinterMapView(self.signin_map_frame, width=1300, height=850, corner_radius=0)
                map_widget.set_address(selected_ride[1])
                map_widget.set_zoom(15)
                map_widget.set_position((start_lat + end_lat) / 2, (start_lng + end_lng) / 2)  # Centralize o mapa
                map_widget.place(relx=0.5, rely=0.5, anchor="center")  # Ajuste x e y conforme necessário
                map_widget.set_marker(start_lat, start_lng, text="Start")
                map_widget.set_marker(end_lat, end_lng, text="End")
                map_widget.set_marker(driver_lat, driver_lng,text="Current location")
                map_widget.set_path(route_coords)
            except Exception as e:
                # Lida com erros ao criar o widget do mapa ou definir os marcadores
                self.signin_riders_feedback.configure(self.signin_riders_feedback, text="Error displaying map", font=("Helvetica", 15, "bold"), text_color="red")
                return
            root.mainloop()
            
            backend.delete_user("passengers", selected_ride[0])
            backend.delete_user("drivers", self.name)
    
    def __new_signin(self):
        backend.delete_user("drivers", self.name)
        self.signin_stats_frame.place_forget()
        self.signin_map_frame.place_forget()
        self.app.build_app()
        
class RiderSignin:
    def __init__(self, app, root, name):
        self.app = app
        self.name = name
        self.price = None
        self.currentbalance = None
        self.signin_stats_frame = ctk.CTkFrame(root, width=400, height=900)
        self.signin_stats_frame_title = ctk.CTkLabel(self.signin_stats_frame, text=f"Welcome {self.name}", font=("Helvetica", 30, "bold"))
        self.signin_trip_frame = ctk.CTkFrame(self.signin_stats_frame, width=300, height=270)
        self.signin_trip_frame_text = ctk.CTkLabel(self.signin_trip_frame, text="Current trip", font=("Helvetica", 15, "bold"))
        self.signin_trip_origin = ctk.CTkEntry(self.signin_trip_frame, width=250, height=24, placeholder_text="insert origin address", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signin_trip_destiny = ctk.CTkEntry(self.signin_trip_frame, width=250, height=24, placeholder_text="insert destiny address", font=("Helvetica", 12, "bold"), corner_radius=12)
        self.signin_trip_price = ctk.CTkLabel(self.signin_trip_frame, text="", font=("Helvetica", 15, "bold"))
        self.signin_trip_calculate_button = ctk.CTkButton(self.signin_trip_frame, width=150, height=24, text="Calculate price", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_calculus, corner_radius=12, state="disabled")
        self.signin_trip_connect_button = ctk.CTkButton(self.signin_trip_frame, width=150, height=24, text="Connect to driver", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_request, corner_radius=12, state="disabled")
        self.signin_trip_update_button = ctk.CTkButton(self.signin_trip_frame, width=150, height=24, text="Update", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_update, corner_radius=12, state="disabled")
        self.signin_trip_finish_button = ctk.CTkButton(self.signin_trip_frame, width=150, height=24, text="Finish ride", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), command=self.__handle_finish, corner_radius=12, state="disabled")
        self.signin_trip_feedback = ctk.CTkLabel(self.signin_trip_frame, text="", font=("Helvetica", 15, "bold"))
        self.signin_map_frame = ctk.CTkFrame(root, width=1350, height=900)
        self.signin_wallet_frame = ctk.CTkFrame(self.signin_stats_frame, width=300, height=400)
        self.signin_wallet_balance = ctk.CTkLabel(self.signin_wallet_frame, text="Your balance:", font=("Helvetica", 20, "bold"))
        self.signin_wallet_money = ctk.CTkLabel(self.signin_wallet_frame, text="", font=("Helvetica", 15, "bold"))
        self.signin_wallet_money_button = ctk.CTkButton(self.signin_wallet_frame, width=150, height=24, text="Show balance", fg_color="DodgerBlue3", hover_color="SteelBlue", font=("Helvetica", 12, "bold"), corner_radius=12, command=self.__handle_balance)
        self.signin_wallet_frame_title = ctk.CTkLabel(self.signin_wallet_frame, text="Wallet", font=("Helvetica", 30, "bold"))
        self.signout_button = ctk.CTkButton(self.signin_stats_frame, width=150, height=24, text="Sign out", fg_color="firebrick3", hover_color="indianred3", font=("Helvetica", 12, "bold"), command=self.__new_signin, corner_radius=12)
    
    def build_signin(self):
        self.signin_stats_frame.place(relx=0.135, rely=0.5, anchor="center")
        self.signin_stats_frame_title.place(relx=0.5, rely=0.1, anchor="center")
        self.signin_trip_frame.place(relx=0.5, rely=0.30, anchor="center")
        self.signin_trip_frame_text.place(relx=0.5, rely=0.10, anchor="center")
        self.signin_trip_origin.place(relx=0.5, rely=0.20, anchor="center")
        self.signin_trip_destiny.place(relx=0.5, rely=0.30, anchor="center")
        self.signin_trip_price.place(relx=0.5, rely=0.40, anchor="center")
        self.signin_trip_calculate_button.place(relx=0.5, rely=0.50, anchor='center')
        self.signin_trip_connect_button.place(relx=0.5, rely=0.6, anchor="center")
        self.signin_trip_update_button.place(relx=0.5, rely=0.7, anchor="center")
        self.signin_trip_finish_button.place(relx=0.5, rely=0.8, anchor="center")
        self.signin_trip_feedback.place(relx=0.5, rely=0.9, anchor="center")
        self.signin_map_frame.place(relx=0.619, rely=0.5, anchor="center")
        self.signin_wallet_frame.place(relx=0.5, rely=0.70, anchor="center")
        self.signin_wallet_balance.place(relx=0.5, rely=0.3, anchor="center")
        self.signin_wallet_money.place(relx=0.5, rely=0.5, anchor="center")
        self.signin_wallet_money_button.place(relx=0.5, rely=0.7, anchor="center")
        self.signin_wallet_frame_title.place(relx=0.5, rely=0.1, anchor="center")
        self.signout_button.place(relx=0.5, rely=0.96, anchor="center")
        self.signin_trip_origin.bind(sequence="<KeyRelease>", command=self.__update_trip_calculate_button)
        self.signin_trip_destiny.bind(sequence="<KeyRelease>", command=self.__update_trip_calculate_button)
    
    def __handle_balance(self):
        self.signin_wallet_money.configure(text=f"Ridecoins:{self.currentbalance}")
    
    def __handle_calculus(self):
        origin = str(self.signin_trip_origin.get())
        destiny = str(self.signin_trip_destiny.get())
        distance, duration, route_coords = backend.get_distance_and_duration(origin, destiny, backend.api_key)

        try:
            start_lat, start_lng = backend.get_coordinates(origin)
            end_lat, end_lng = backend.get_coordinates(destiny)
            
            # Verifica se as coordenadas foram encontradas
            if start_lat is None or start_lng is None or end_lat is None or end_lng is None:
                self.signin_trip_price.configure(self.signin_trip_frame, text="One of the provided addresses is not valid", font=("Helvetica", 15, "bold"), text_color="red")
                return
            
            # Converte as coordenadas para float
            start_lat = float(start_lat)
            start_lng = float(start_lng)
            end_lat = float(end_lat)
            end_lng = float(end_lng)
            
        except (TypeError, ValueError) as e:
            # Lida com erros de conversão e outros erros
            self.signin_trip_price.configure(self.signin_trip_frame, text="One of the provided addresses is not valid", font=("Helvetica", 15, "bold"), text_color="red")
            return
        
        root = self.signin_map_frame.winfo_toplevel()
        root.title('mapa')
        try:
            map_widget = tkintermapview.TkinterMapView(self.signin_map_frame, width=1300, height=850, corner_radius=0)
            map_widget.set_address(origin)
            map_widget.set_zoom(15)
            map_widget.set_position((start_lat + end_lat) / 2, (start_lng + end_lng) / 2)  # Centralize o mapa
            map_widget.place(relx=0.5, rely=0.5, anchor="center")  # Ajuste x e y conforme necessário
            map_widget.set_marker(start_lat, start_lng, text="Start")
            map_widget.set_marker(end_lat, end_lng, text="End")
            map_widget.set_path(route_coords)
        except Exception as e:
            # Lida com erros ao criar o widget do mapa ou definir os marcadores
            self.signin_trip_price.configure(self.signin_trip_frame, text="Error displaying map", font=("Helvetica", 15, "bold"), text_color="red")
            return

        if distance == "error":
            self.signin_trip_price.configure(self.signin_trip_frame, text="One of the provided addresses is not valid", font=("Helvetica", 15, "bold"), text_color="red")
        else:
            price = backend.price(distance, duration)
            self.price = price
            distance="{:.2f}".format(price)
            duration="{:.2f}".format(duration)
            price="{:.2f}".format(price)
            self.signin_trip_price.configure(self.signin_trip_frame, text=f"U${price} | {distance} km | {duration} min", font=("Helvetica", 15, "bold"), text_color="white")
            self.signin_trip_connect_button.configure(state="normal")
        root.mainloop()
        
    def __handle_request(self):
        origin = str(self.signin_trip_origin.get())
        destiny = str(self.signin_trip_destiny.get())
        backend_feedback = backend.passenger_request(self.name, origin, destiny)
        if backend_feedback == "connect":
            self.signin_trip_feedback.configure(text="Connection problem, try again later", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback == "error":
            self.signin_trip_feedback.configure(text="There was a problem with the request", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback == "success":
            self.signin_trip_feedback.configure(text="Connecting to driver", font=("Helvetica", 15, "bold"), text_color="green")
            self.signin_trip_update_button.configure(state="normal")
    
    def __handle_update(self):
        backend_feedback = backend.update_status(self.name)
        if backend_feedback == "error":
            self.signin_trip_feedback.configure(text="There was a problem with the update", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback == "unconfirmed":
            self.signin_trip_feedback.configure(text="Ride not found yet", font=("Helvetica", 15, "bold"), text_color="red")
        if backend_feedback == "confirmed":
            self.signin_trip_feedback.configure(text="Ride confirmed, wait for driver", font=("Helvetica", 15, "bold"), text_color="green")
            self.signin_trip_finish_button.configure(state="normal")
    
    def __handle_finish(self):
        self.signin_trip_feedback.configure(text="Thanks for using Ddrive", text_color="white")
        account = backend.get_account(self.name)
        account_driver = backend.get_account(backend.get_driver_name(self.name))
        if account == "connect" or account_driver == "connect":
            self.signin_wallet_money.configure(text="There was a problem, try again later", text_color="red")
        else:
            backend.send_information(account, account_driver, float(self.price), "0x4bbbf85ce3377467afe5d46f804f221813b2bb87f24d81f60f1fcdbf7cbf4356")
        self.currentbalance=backend.fetch()[str(account)]
        backend.delete_user("rides", self.name)
    
    def __update_trip_calculate_button(self, event=None):
        user_origin = self.signin_trip_origin.get()
        user_destiny = self.signin_trip_destiny.get()
        if user_origin and user_destiny:
            self.signin_trip_calculate_button.configure(state="normal")
    
    def __new_signin(self):
        backend.delete_user("passengers", self.name)
        self.signin_stats_frame.place_forget()
        self.signin_map_frame.place_forget()
        self.app.build_app()