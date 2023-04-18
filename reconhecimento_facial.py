import cv2
import face_recognition

class ReconhecimentoFacial:
    def __init__(self):
        self.encodings_conhecidos = []
        self.nomes_conhecidos = []

    def cadastrar_pessoa(self, imagem_path, nome):
        imagem = face_recognition.load_image_file(imagem_path)
        encoding = face_recognition.face_encodings(imagem)[0]
        self.encodings_conhecidos.append(encoding)
        self.nomes_conhecidos.append(nome)

    def reconhecer_pessoa(self, imagem):
        faces = face_recognition.face_locations(imagem)
        encodings = face_recognition.face_encodings(imagem, faces)
        nome = "Desconhecido"
        for encoding in encodings:
            matches = face_recognition.compare_faces(self.encodings_conhecidos, encoding)
            if True in matches:
                index = matches.index(True)
                nome = self.nomes_conhecidos[index]
                break
        return nome
