from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, computed_field, Field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
import json


app = FastAPI()


# define a Patient pydantic model
class Patient(BaseModel):

    id: Annotated[str, Field(..., description = 'Patient ID', example = 'P001')]
    name: Annotated[str, Field(..., description = 'Patient Name', example = 'John Doe')]
    age: Annotated[int, Field(..., description = 'Patient Age', gt = 0, lt = 150,example = 30)]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description = 'Patient Gender', example = 'Male')]
    height: Annotated[float, Field(..., description = 'Patient Height in cm', gt = 0, example = 175.5)]
    weight: Annotated[float, Field(..., description = 'Patient Weight in kg', gt = 0, example = 70.0)]

    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        bmi_value = self.weight / (height_in_meters ** 2)
        return round(bmi_value, 2)


    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi_value < 24.9:
            return 'Normal weight'
        elif 25 <= bmi_value < 29.9:
            return 'Overweight'
        else:
            return 'Obesity'
        

class PatientUpdate(BaseModel):
    id: Annotated[Optional[str], Field(default=None)]
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open('patients.json') as f:
        data = json.load(f)
    
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return {"message": "Patients Management System: FastAPI Application!"}


@app.get('/about')
def about():
    return {"message": "Fully functional FastAPI application for managing patient records."}


@app.get('/viewpatients')
def view_patients():
    data = load_data()
    return data



@app.get('/viewpatient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'Enter the ID of the Patient(DB)', Example = 'P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    # return {"error" : "User Not Found!!"}
    raise HTTPException(status_code=404, detail = 'Patient Not Found!')
        


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail = f'Invalid Field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Not a valid order, order should be asc or desc')
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data



@app.post('/createpatient')
def create_patient(patient: Patient):
    
    data = load_data()

    # check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists!')

    # add new patient
    data[patient.id] = patient.model_dump(exclude = ['id'])

    # save data back to json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully!'})




# Update a patient record
@app.put('/updatepatient/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    # load existing data
    data = load_data()

    # check if patient with given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found!')

    # get existing patient details
    existing_patient = data[patient_id]

    # update patient details
    updated_patient = patient_update.model_dump(exclude_unset=True)

    # merge existing patient data with updated data
    for key, value in updated_patient.items():
        existing_patient[key] = value

    # existing_patient_info -> pydantic object -> update bmi + verdict 
    # dict -> pydantic object   
    existing_patient['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient)

    # pydantic object -> dict
    existing_patient = patient_pydantic_obj.model_dump(exclude = ['id'])


    data[patient_id] = existing_patient

    save_data(data)

    return {'message': 'Patient updated successfully!'}



@app.delete('/deletepatient/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found!')

    # delete patient
    del data[patient_id]

    # save data back to json file
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully!'})









