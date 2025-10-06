from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import requests
import base64
from services.face_verification import verify_faces

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    return {"message": "Face API is running!"}


# @app.route('/verify-face', methods=['POST'])
# def verify_face():
#     try:
#         profile_url = request.form.get("profileImageUrl")
#         live_image = request.files.get("liveImage")

#         if not profile_url or not live_image:
#             return jsonify({"error": "Missing profileImageUrl or liveImage"}), 400

#         # Save live image temporarily
#         live_image_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
#         live_image.save(live_image_path)

#         # Handle profile image
#         profile_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")

#         if profile_url.startswith("http"):
#             # Remote image
#             r = requests.get(profile_url, stream=True, timeout=10)
#             r.raise_for_status()
#             with open(profile_path, 'wb') as f:
#                 f.write(r.content)
#         elif profile_url.startswith("data:image"):  # base64 image
#             header, encoded = profile_url.split(",", 1)
#             data = base64.b64decode(encoded)
#             with open(profile_path, 'wb') as f:
#                 f.write(data)
#         else:
#             # Local path
#             profile_path = profile_url

#         # Compare faces
#         result = verify_faces(profile_path, live_image_path)

#         # Clean up only temp files (skip if local path)
#         if profile_url.startswith("http") or profile_url.startswith("data:image"):
#             os.remove(profile_path)
#         os.remove(live_image_path)

#         return jsonify(result)

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": "Face verification failed"}), 500

@app.route("/encode-face", methods=["POST"])
def encode_face():
    try:
        import face_recognition, requests, numpy as np, uuid, os
        from PIL import Image
        from io import BytesIO

        image_file = request.files.get("profileImage")
        image_url = request.json.get("image_url") if request.is_json else None

        if not image_file and not image_url:
            return jsonify({"error": "Profile image missing"}), 400

        # Save or download the image
        path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")

        if image_file:
            image_file.save(path)
        else:
            # Download the image from the given URL
            resp = requests.get(image_url, stream=True)
            if resp.status_code != 200:
                return jsonify({"error": "Failed to download image"}), 400
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            img.save(path)

        # Process face encoding
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        os.remove(path)

        if len(encodings) == 0:
            return jsonify({"error": "No face detected"}), 400

        encoding_list = encodings[0].tolist()
        return jsonify({"encoding": encoding_list})

    except Exception as e:
        print("Error in /encode-face:", e)
        return jsonify({"error": "Failed to encode face"}), 500


@app.route("/verify-face", methods=["POST"])
def verify_face():
    try:
        live_image = request.files.get("liveImage")
        profile_encoding = request.form.get("profileEncoding")  # JSON array from Express

        if not live_image or not profile_encoding:
            return jsonify({"error": "Missing live image or encoding"}), 400

        import json, numpy as np, os, face_recognition, uuid

        # Convert the stored encoding from JSON → numpy array
        profile_encoding = np.array(json.loads(profile_encoding))

        # Save live image temporarily
        live_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
        live_image.save(live_path)

        # Extract encoding directly (no resize)
        live_enc = face_recognition.face_encodings(face_recognition.load_image_file(live_path))
        os.remove(live_path)

        if len(live_enc) == 0:
            return jsonify({"error": "No face detected in live image"}), 400

        live_enc = live_enc[0]

        # Compare
        match = face_recognition.compare_faces([profile_encoding], live_enc)[0]
        confidence = (1 - face_recognition.face_distance([profile_encoding], live_enc)[0]) * 100

        # Optional threshold for clarity
        threshold = 50
        match = confidence >= threshold

        return jsonify({
            "match": bool(match),
            "confidence": float(confidence)
        })

    except Exception as e:
        print(e)
        return jsonify({"error": "Face verification failed"}), 500



# @app.route("/verify-face", methods=["POST"]) ### fully WORKINGGGGGG
# def verify_face():
#     try:
#         live_image = request.files.get("liveImage")
#         profile_encoding = request.form.get("profileEncoding")

#         if not live_image or not profile_encoding:
#             return jsonify({"error": "Missing live image or encoding"}), 400

#         import json, numpy as np
#         profile_encoding = np.array(json.loads(profile_encoding))

#         live_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
#         live_image.save(live_path)

#         from PIL import Image
#         img = Image.open(live_path).resize((320, 240))
#         img.save(live_path)

#         import face_recognition
#         live_enc = face_recognition.face_encodings(face_recognition.load_image_file(live_path))
#         os.remove(live_path)

#         if len(live_enc) == 0:
#             return jsonify({"error": "No face detected in live image"}), 400

#         live_enc = live_enc[0]

#         match = face_recognition.compare_faces([profile_encoding], live_enc)[0]
#         confidence = (1 - face_recognition.face_distance([profile_encoding], live_enc)[0]) * 100

#         # ✅ Convert NumPy → native types
#         return jsonify({
#             "match": bool(match),
#             "confidence": float(confidence)
#         })

#     except Exception as e:
#         import traceback
#         print("❌ FACE VERIFY ERROR:")
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500


# @app.route("/verify-face", methods=["POST"])
# def verify_face():
#     try:
#         live_image = request.files.get("liveImage")
#         profile_encoding = request.form.get("profileEncoding")  # JSON array from Express

#         if not live_image or not profile_encoding:
#             return jsonify({"error": "Missing live image or encoding"}), 400

#         import json, numpy as np
#         profile_encoding = np.array(json.loads(profile_encoding))

#         live_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
#         live_image.save(live_path)

#         from PIL import Image
#         img = Image.open(live_path).resize((320, 240))
#         img.save(live_path)

#         import face_recognition
#         live_enc = face_recognition.face_encodings(face_recognition.load_image_file(live_path))
#         os.remove(live_path)

#         if len(live_enc) == 0:
#             return jsonify({"error": "No face detected in live image"}), 400

#         live_enc = live_enc[0]

#         match = face_recognition.compare_faces([profile_encoding], live_enc)[0]
#         confidence = (1 - face_recognition.face_distance([profile_encoding], live_enc)[0]) * 100

#         return jsonify({"match": match, "confidence": confidence})

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Face verification failed"}), 500



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3001, debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port, debug=True)