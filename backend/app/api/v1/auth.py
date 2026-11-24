from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserRole
from app.models.audit import AuditLog
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut, UserUpdate

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, request: Request, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # First registered user becomes OWNER for easy administration
    user_count = db.query(User).count()
    role = UserRole.OWNER if user_count == 0 else UserRole.USER

    hashed_pw = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name or user_in.email.split("@")[0],
        role=role,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Audit log
    audit = AuditLog(
        user_id=user.id,
        action="USER_REGISTER",
        resource_type="user",
        resource_id=user.id,
        ip_address=request.client.host if request.client else None
    )
    db.add(audit)
    db.commit()

    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserOut.model_validate(user))

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is deactivated.")

    # Audit log
    audit = AuditLog(
        user_id=user.id,
        action="USER_LOGIN",
        resource_type="user",
        resource_id=user.id,
        ip_address=request.client.host if request.client else None
    )
    db.add(audit)
    db.commit()

    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer", user=UserOut.model_validate(user))

@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_current_user(
    update_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if update_in.full_name:
        current_user.full_name = update_in.full_name
    if update_in.password:
        current_user.hashed_password = hash_password(update_in.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user
