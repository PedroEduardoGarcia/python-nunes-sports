import os
from fastapi import Body, FastAPI, HTTPException, Path, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List,  AsyncGenerator
from models import Product
from repositories import PostgresRepository
from services import ProductService

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = PostgresRepository(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

product_service = ProductService(pool=repo.pool)

async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager to manage startup and shutdown events."""
    await repo.connect()
    global product_service
    product_service = ProductService(repo.pool)
    yield
    await repo.close()


app = FastAPI(lifespan=lifespan)

@app.post("/api/test")
async def post_message(data: Dict[str, Any]) -> Dict[str, str]:
    return {"message": f"Hello from the POST endpoint! You sent: {data['username']}"}

@app.post("/api/products/")
async def create_product(product: Product) -> Dict[str, int]:
    """Create a new product."""
    if not product_service:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service not available")
    
    product_id = await product_service.create_product(product)
    if product_id:
        return {"id": product_id}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Product creation failed")

@app.get("/api/products/{product_id}", response_model=Product)
async def read_product(product_id: int = Path(..., gt=0)) -> Product:
    product = await product_service.get_product_by_id(product_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/api/products/{product_id}", response_model=Dict[str, str])
async def update_product(product_id: int, product: Product) -> Dict[str, str]:
    success = await product_service.update_product(product_id, product)
    if success:
        return {"detail": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/api/products/{product_id}", response_model=Dict[str, str])
async def delete_product(product_id: int) -> Dict[str, str]:
    success = await product_service.delete_product(product_id)
    if success:
        return {"detail": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/products/", response_model=List[Product])
async def list_products() -> List[Product]:
    products = await product_service.list_products()
    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)