import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import dlib
import os
import numpy as np
import webbrowser
import time


class FacialAuthenticationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Autenticação Facial")

        self.authenticate_button = tk.Button(self.root, text="Autenticar", command=self.authenticate)
        self.authenticate_button.pack(side=tk.RIGHT)

        self.register_button = tk.Button(self.root, text="Cadastro", command=self.register)
        self.register_button.pack(side=tk.RIGHT)

        self.update_user_button = tk.Button(self.root, text="Atualizar Usuário", command=self.update_user)
        self.update_user_button.pack(side=tk.RIGHT)

        self.camera_frame = tk.Label(self.root)
        self.camera_frame.pack(side=tk.LEFT)

        self.face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
        self.users_file = "usuarios.txt"
        self.users_folder = "usuarios"

        self.load_users()
        self.start_camera()

    def load_users(self):
        self.users = []
        with open(self.users_file, "r") as file:
            for line in file:
                if "," not in line:
                    continue
                name, access_level = line.strip().split(",")
                self.users.append({"name": name, "access_level": int(access_level)})

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir a câmera")
            self.root.destroy()
            return
        self.show_camera()

    def show_camera(self):
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Erro", "Não foi possível capturar a imagem da câmera")
            self.root.destroy()
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Pré-processamento
        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.detector(gray)
        for face in faces:
            landmarks = self.predictor(gray, face)
            left, top, right, bottom = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

            for n in range(5):
                x, y = landmarks.part(n).x, landmarks.part(n).y
                cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

            face_descriptor = self.face_descriptor(frame, landmarks)

            name = self.match_face(face_descriptor)

            if name:
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Usuario nao Cadastrado", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 0, 255), 2)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        if hasattr(self, 'camera_label'):
            self.camera_label.configure(image=imgtk)
            self.camera_label.image = imgtk
        else:
            self.camera_label = tk.Label(self.root, image=imgtk)
            self.camera_label.image = imgtk
            self.camera_label.pack()

        self.camera_frame.after(10, self.show_camera)

    def face_descriptor(self, frame, landmarks):
        face_chip = dlib.get_face_chip(frame, landmarks)
        face_descriptor = self.face_recognizer.compute_face_descriptor(face_chip)
        return face_descriptor

    def match_face(self, face_descriptor):
        for user in self.users:
            user_folder = os.path.join(self.users_folder, user["name"])
            if not os.path.exists(user_folder):
                continue

            for file_name in os.listdir(user_folder):
                image_path = os.path.join(user_folder, file_name)
                registered_descriptor = self.load_descriptor(image_path)

                face_descriptor_np = np.array(face_descriptor)
                registered_descriptor_np = np.array(registered_descriptor)

                distance = np.linalg.norm(face_descriptor_np - registered_descriptor_np)
                if distance < 0.7:
                    return user["name"]

        return None

    def load_descriptor(self, image_path):
        img = dlib.load_rgb_image(image_path)
        landmarks = self.predictor(img, dlib.rectangle(0, 0, img.shape[1], img.shape[0]))
        face_descriptor = self.face_descriptor(img, landmarks)
        return face_descriptor

    def authenticate(self):
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Erro", "Não foi possível capturar a imagem da câmera")
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.detector(gray)
        for face in faces:
            landmarks = self.predictor(gray, face)
            face_descriptor = self.face_descriptor(frame, landmarks)
            name = self.match_face(face_descriptor)

            if name:
                user = next((user for user in self.users if user["name"] == name), None)
                if user["access_level"] == 3:
                    file_path = "index/inicio.html"
                elif user["access_level"] == 2:
                    file_path = "index/informacoes.html"
                elif user["access_level"] == 1:
                    file_path = "index/cadastro.html"

                url = f"file://{os.path.abspath(file_path)}"
                webbrowser.open_new_tab(url)

            else:
                messagebox.showinfo("Autenticação", "Usuário não cadastrado")

    def register(self):
        password = simpledialog.askstring("Cadastro", "Digite a senha de administrador:")
        if password != "12345":
            messagebox.showinfo("Cadastro", "Senha inválida")
            return

        name = simpledialog.askstring("Cadastro", "Digite o nome do usuário:")
        access_level = simpledialog.askinteger("Cadastro", "Digite o nível de acesso (1, 2 ou 3):")
        if access_level not in [3, 2, 1]:
            messagebox.showinfo("Cadastro", "Nível de acesso inválido")
            return

        if any(user["name"] == name for user in self.users):
            messagebox.showinfo("Cadastro", "Usuário já cadastrado")
            return

        user = {"name": name, "access_level": access_level}
        self.users.append(user)

        user_folder = os.path.join(self.users_folder, name)
        os.makedirs(user_folder, exist_ok=True)

        messagebox.showinfo("Cadastro", "Clique aqui para tirar as fotos")
        self.take_photos(user_folder)

        with open(self.users_file, "a") as file:
            file.write(f"{name},{access_level}\n")

    def take_photos(self, user_folder):
        for i in range(20):
            ret, frame = self.cap.read()
            if not ret:
                messagebox.showerror("Erro", "Não foi possível capturar a imagem da câmera")
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = self.detector(gray)
            if len(faces) != 1:
                messagebox.showinfo("Cadastro", "Erro ao capturar foto. Tente novamente.")
                return

            face = faces[0]
            landmarks = self.predictor(gray, face)
            face_descriptor = self.face_descriptor(frame, landmarks)

            img = dlib.get_face_chip(frame, landmarks)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            file_path = os.path.join(user_folder, f"{i}.jpg")
            cv2.imwrite(file_path, img)

            time.sleep(0.5)

        messagebox.showinfo("Cadastro", "Cadastro concluído com sucesso!")

    def update_user(self):
        password = simpledialog.askstring("Atualizar Usuário", "Digite a senha de administrador:")
        if password != "12345":
            messagebox.showinfo("Atualizar Usuário", "Senha inválida")
            return

        name = simpledialog.askstring("Atualizar Usuário", "Digite o nome do usuário que deseja atualizar:")
        user = next((user for user in self.users if user["name"] == name), None)
        if not user:
            messagebox.showinfo("Atualizar Usuário", "Usuário não encontrado")
            return

        action = simpledialog.askstring("Atualizar Usuário", "Deseja alterar ou excluir o usuário? (alterar/excluir)")
        if action == "alterar":
            new_name = simpledialog.askstring("Atualizar Usuário", "Digite o novo nome do usuário:")
            new_access_level = simpledialog.askinteger("Atualizar Usuário",
                                                       "Digite o novo nível de acesso (1, 2 ou 3):")
            if new_access_level not in [3, 2, 1]:
                messagebox.showinfo("Atualizar Usuário", "Nível de acesso inválido")
                return

            user["name"] = new_name
            user["access_level"] = new_access_level

            with open(self.users_file, "w") as file:
                for user in self.users:
                    file.write(f"{user['name']},{user['access_level']}\n")

            messagebox.showinfo("Atualizar Usuário", "Usuário atualizado com sucesso!")
        elif action == "excluir":
            self.users.remove(user)

            with open(self.users_file, "w") as file:
                for user in self.users:
                    file.write(f"{user['name']},{user['access_level']}\n")

            user_folder = os.path.join(self.users_folder, name)
            if os.path.exists(user_folder):
                for file_name in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file_name)
                    os.remove(file_path)
                os.rmdir(user_folder)

            messagebox.showinfo("Atualizar Usuário", "Usuário excluído com sucesso!")


root = tk.Tk()
app = FacialAuthenticationTool(root)
root.mainloop()
