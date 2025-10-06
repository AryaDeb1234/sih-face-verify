import face_recognition

def verify_faces(profile_path, live_path):
    try:
        profile_img = face_recognition.load_image_file(profile_path)
        live_img = face_recognition.load_image_file(live_path)

        profile_encodings = face_recognition.face_encodings(profile_img)
        live_encodings = face_recognition.face_encodings(live_img)

        if len(profile_encodings) == 0 or len(live_encodings) == 0:
            return {"match": False, "confidence": 0.0, "error": "No face detected"}

        # Take the first face found in each
        match_results = face_recognition.compare_faces(
            [profile_encodings[0]], live_encodings[0]
        )
        face_distance = face_recognition.face_distance(
            [profile_encodings[0]], live_encodings[0]
        )[0]

        confidence = round((1 - face_distance) * 100, 2)

        return {"match": bool(match_results[0]), "confidence": confidence}

    except Exception as e:
        print("Verification error:", e)
        return {"match": False, "confidence": 0.0, "error": str(e)}
