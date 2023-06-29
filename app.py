from typing import List
import torch
from fastapi import FastAPI, File, Body
from facenet_pytorch import MTCNN, InceptionResnetV1
from pydantic import BaseModel
from utils import get_faces

from db.operations import (
    create_embeddings_table, 
    insert_embedding, 
    find_most_similar_embedding
)

app = FastAPI()

# Initialize the MTCNN face detection model and InceptionResnetV1 face recognition model
mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()


create_embeddings_table()

class UserResponse(BaseModel):
    user_id: str


@app.post("/image_to_user", response_model=List[str])
async def image_to_user(image: bytes = File(...)):
    # Extract faces from the image
    faces = get_faces(image)

    user_ids = []

    for face in faces:
        # Convert the face data from a numpy array to a PyTorch tensor
        face_tensor = torch.from_numpy(face).permute(2, 0, 1).float()

        # Compute the embedding for the face using the InceptionResnetV1 model
        embedding = resnet(face_tensor.unsqueeze(0)).detach().numpy().reshape(-1)

        most_similar_id = find_most_similar_embedding(embedding)

        user_ids.append(UserResponse(user_id=most_similar_id))

    return user_ids


@app.post("/user", response_model=UserResponse)
async def create_user(image: bytes = File(...), user_id: str = Body(...)):
    # Extract faces from the image
    faces = get_faces(image)

    for face in faces:
        # Convert the face data from a numpy array to a PyTorch tensor
        face_tensor = torch.from_numpy(face).permute(2, 0, 1).float()

        # Compute the embedding for the face using the InceptionResnetV1 model
        embedding = resnet(face_tensor.unsqueeze(0)).detach().squeeze().numpy()

        insert_embedding(embedding, user_id)

    # Your code to create the user profile
    return {"user_id": user_id}


@app.delete("/user/{user_id}", response_model=UserResponse)
async def delete_user(user_id: str):
    # Your code to delete the user profile and associated image embedding(s)
    return {"user_id": user_id}
