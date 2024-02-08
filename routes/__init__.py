from fastapi import APIRouter
from . import about_me, contact_me, loan_approval_prediction, my_projects, secure_data_transfer_and_information_hidding

router = APIRouter()

router.include_router(about_me.router)
router.include_router(contact_me.router)
router.include_router(loan_approval_prediction.router)
router.include_router(my_projects.router)
router.include_router(secure_data_transfer_and_information_hidding.router)