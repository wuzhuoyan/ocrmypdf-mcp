from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check() -> str:
    """
    健康检查接口
    :return: json
    """
    return "ok"