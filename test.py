import face_recognition

image_path = r"C:\Users\aryad\OneDrive\Desktop\wallpaper\man.jpg"  # Use raw string with r""
image = face_recognition.load_image_file(image_path)
faces = face_recognition.face_locations(image)
print("Faces found:", len(faces))
