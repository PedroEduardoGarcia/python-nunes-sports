import React, { useState } from "react";

interface Product {
  id: number;
  name: string;
  code: string;
  description: string;
  category: string;
  price: number;
  created_at: string;
}

enum Tab {
  Search,
  Create,
  CreateRandom,
  Delete,
  Update,
}

const ProductTable: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>(Tab.Search);
  const [productId, setProductId] = useState<string>("");
  const [deleteProductId, setDeleteProductId] = useState<string>("");
  const [allProducts, setAllProducts] = useState<Product[]>([]);
  const [newProduct, setNewProduct] = useState<Omit<Product, "id">>({
    name: "",
    code: "",
    description: "",
    category: "",
    price: 0,
    created_at: new Date().toISOString(),
  });
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [createdProduct, setCreatedProduct] = useState<Product | null>(null);
  const [deleteSuccessMessage, setDeleteSuccessMessage] = useState<
    string | null
  >(null);

  const handleSearchProduct = async () => {
    try {
      const response = await fetch(
        `http://44.201.89.150:3000/api/products/${productId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product = await response.json();
      setNewProduct({
        name: data.name,
        code: data.code,
        description: data.description,
        category: data.category,
        price: data.price,
        created_at: data.created_at,
      });
    } catch (error) {
      console.error("Error fetching product by ID:", error);
    }
  };

  const handleUpdateProduct = async () => {
    try {
      if (
        !newProduct.name ||
        !newProduct.code ||
        !newProduct.description ||
        !newProduct.category ||
        newProduct.price <= 0
      ) {
        console.error("Please fill out all fields correctly.");
        return;
      }

      const response = await fetch(
        `http://44.201.89.150:3000/api/products/${productId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newProduct),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      setSuccessMessage("Product updated successfully.");
    } catch (error) {
      console.error("Error updating product:", error);
    }
  };

  const handleFetchAllProducts = async () => {
    try {
      const response = await fetch("http://44.201.89.150:3000/api/products/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product[] = await response.json();
      setAllProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleFetchById = async () => {
    try {
      const response = await fetch(
        `http://44.201.89.150:3000/api/products/${productId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product = await response.json();
      setAllProducts([data]);
    } catch (error) {
      console.error("Error fetching product by ID:", error);
    }
  };

  const handleCreateProduct = async () => {
    try {
      if (
        !newProduct.name ||
        !newProduct.code ||
        !newProduct.description ||
        !newProduct.category ||
        newProduct.price <= 0
      ) {
        console.error("Please fill out all fields correctly.");
        return;
      }

      const response = await fetch("http://44.201.89.150:3000/api/products/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...newProduct,
          created_at: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product = await response.json();
      setAllProducts([...allProducts, data]);
      setSuccessMessage(`Product created successfully with ID: ${data.id}`);
    } catch (error) {
      console.error("Error creating product:", error);
    }
  };

  const handleCreateRandomProduct = async () => {
    try {
      const response = await fetch("http://44.201.89.150:3000/api/products_test/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data: Product = await response.json();
      setCreatedProduct(data);
    } catch (error) {
      console.error("Error creating random product:", error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewProduct((prevProduct) => ({
      ...prevProduct,
      [name]: name === "price" ? parseFloat(value) : value,
    }));
  };

  const handleDeleteProduct = async () => {
    try {
      const response = await fetch(
        `http://44.201.89.150:3000/api/products/${deleteProductId}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setDeleteSuccessMessage(data.detail);
      setAllProducts(
        allProducts.filter(
          (product) => product.id !== parseInt(deleteProductId)
        )
      );
    } catch (error) {
      console.error("Error deleting product:", error);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Nunes Sports Product Management</h1>

      <ul className="nav nav-tabs">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === Tab.Search ? "active" : ""}`}
            onClick={() => setActiveTab(Tab.Search)}
          >
            Search
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === Tab.Create ? "active" : ""}`}
            onClick={() => setActiveTab(Tab.Create)}
          >
            Create
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${
              activeTab === Tab.CreateRandom ? "active" : ""
            }`}
            onClick={() => setActiveTab(Tab.CreateRandom)}
          >
            Create Random
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === Tab.Update ? "active" : ""}`}
            onClick={() => setActiveTab(Tab.Update)}
          >
            Update
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === Tab.Delete ? "active" : ""}`}
            onClick={() => setActiveTab(Tab.Delete)}
          >
            Delete
          </button>
        </li>
      </ul>

      <div className="tab-content mt-3">
        {activeTab === Tab.Search && (
          <>
            <div className="mb-4">
              <input
                type="text"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
                placeholder="Enter Product ID"
                className="form-control mb-2"
              />
              <button
                onClick={handleFetchById}
                className="btn btn-primary mr-2"
              >
                Get Product by ID
              </button>
              <button
                onClick={handleFetchAllProducts}
                className="btn btn-secondary float-end"
              >
                List All Products
              </button>
            </div>

            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Code</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Price</th>
                    <th>Created At</th>
                  </tr>
                </thead>
                <tbody>
                  {allProducts.map((product) => (
                    <tr key={product.code}>
                      <td>{product.id}</td>
                      <td>{product.name}</td>
                      <td>{product.code}</td>
                      <td>{product.description}</td>
                      <td>{product.category}</td>
                      <td>{product.price}</td>
                      <td>{new Date(product.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {activeTab === Tab.Create && (
          <div>
            <h3>Create New Product</h3>
            <div className="form-group">
              <input
                type="text"
                name="name"
                value={newProduct.name}
                onChange={handleInputChange}
                placeholder="Enter Product Name"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="code"
                value={newProduct.code}
                onChange={handleInputChange}
                placeholder="Enter Product Code"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="description"
                value={newProduct.description}
                onChange={handleInputChange}
                placeholder="Enter Product Description"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="category"
                value={newProduct.category}
                onChange={handleInputChange}
                placeholder="Enter Product Category"
                className="form-control mb-2"
              />
              <input
                type="number"
                name="price"
                value={newProduct.price || ""}
                onChange={handleInputChange}
                placeholder="Enter Product Price"
                className="form-control mb-2"
              />
            </div>

            <div className="d-flex justify-content-end">
              <button onClick={handleCreateProduct} className="btn btn-success">
                Create Product
              </button>
            </div>

            {successMessage && (
              <div className="alert alert-success mt-3">{successMessage}</div>
            )}
          </div>
        )}

        {activeTab === Tab.CreateRandom && (
          <div>
            <h3>Create Random Product</h3>
            <button
              onClick={handleCreateRandomProduct}
              className="btn btn-success"
            >
              Create Random Product
            </button>
            {createdProduct && (
              <div className="mt-3">
                <h4>Created Product:</h4>
                <p>
                  <strong>Name:</strong> {createdProduct.name}
                </p>
                <p>
                  <strong>Code:</strong> {createdProduct.code}
                </p>
                <p>
                  <strong>Description:</strong> {createdProduct.description}
                </p>
                <p>
                  <strong>Category:</strong> {createdProduct.category}
                </p>
                <p>
                  <strong>Price:</strong> ${createdProduct.price}
                </p>
                <p>
                  <strong>Created At:</strong>{" "}
                  {new Date(createdProduct.created_at).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === Tab.Delete && (
          <div>
            <h3>Delete Product</h3>
            <div className="form-group">
              <input
                type="text"
                value={deleteProductId}
                onChange={(e) => setDeleteProductId(e.target.value)}
                placeholder="Enter Product ID to Delete"
                className="form-control mb-2"
              />
            </div>
            <div className="d-flex justify-content-end">
              <button onClick={handleDeleteProduct} className="btn btn-danger">
                Delete Product
              </button>
            </div>
            {deleteSuccessMessage && (
              <div className="alert alert-success mt-3">
                {deleteSuccessMessage}
              </div>
            )}
          </div>
        )}

        {activeTab === Tab.Update && (
          <div>
            <h3>Update Product</h3>
            <div className="form-group">
              <input
                type="text"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
                placeholder="Enter Product ID"
                className="form-control mb-2"
              />
              <button
                onClick={handleSearchProduct}
                className="btn btn-primary mb-4"
              >
                Search Product by ID
              </button>

              <input
                type="text"
                name="name"
                value={newProduct.name}
                onChange={handleInputChange}
                placeholder="Enter Product Name"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="code"
                value={newProduct.code}
                onChange={handleInputChange}
                placeholder="Enter Product Code"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="description"
                value={newProduct.description}
                onChange={handleInputChange}
                placeholder="Enter Product Description"
                className="form-control mb-2"
              />
              <input
                type="text"
                name="category"
                value={newProduct.category}
                onChange={handleInputChange}
                placeholder="Enter Product Category"
                className="form-control mb-2"
              />
              <input
                type="number"
                name="price"
                value={newProduct.price || ""}
                onChange={handleInputChange}
                placeholder="Enter Product Price"
                className="form-control mb-2"
              />
            </div>

            <div className="d-flex justify-content-end">
              <button onClick={handleUpdateProduct} className="btn btn-success">
                Update Product
              </button>
            </div>

            {successMessage && (
              <div className="alert alert-success mt-3">{successMessage}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductTable;
